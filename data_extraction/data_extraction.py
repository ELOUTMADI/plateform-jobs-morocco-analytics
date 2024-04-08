import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException , TimeoutException
from selenium.webdriver.common.by import By
import json
from data_ingestion.data_lake import *
from hdfs import InsecureClient
from datetime import datetime
def login(driver):
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

    # Use By.ID to find elements by ID
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')

    username = 'faridelkhamini@gmail.com'
    password = 'Aa.123456!'

    for char in username:
        username_field.send_keys(char)
        time.sleep(random.uniform(0.2, 0.3))
    for char in password:
        password_field.send_keys(char)
        time.sleep(random.uniform(0.2, 0.3))

    # Simulate pressing Enter after typing the password
    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN)
    actions.perform()

    # Wait for the login to complete (you may need to adjust the wait conditions)
    WebDriverWait(driver, 10).until(EC.url_contains("linkedin.com"))

    return driver  # Return the driver after login

def get_page_details(driver):
    try:
        pages = driver.find_element(By.XPATH, "//ul[contains(@class,'artdeco-pagination__pages--number')]")
        lists_of_pages = pages.find_elements(By.XPATH, "//li[contains(@class,'artdeco-pagination__indicator')]")
        return lists_of_pages
    except NoSuchElementException:
        return None


def get_job_containers_in_page(driver):
    try:
        job_listings_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[contains(@class,"scaffold-layout__list-container")]'))
        )
        job_elements = job_listings_container.find_elements(By.XPATH, './/div[contains(@class,"job-card-container--clickable")]')
        return job_elements

    except StaleElementReferenceException:
        # Retry if StaleElementReferenceException occurs
        pass


def find_element_with_retry(driver, xpath, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return element.text  # Return the text as soon as it's successfully retrieved
        except StaleElementReferenceException:
            if attempt < max_attempts - 1:
                time.sleep(1)  # Brief pause to give the page a chance to settle
                continue  # Retry finding the element
            else:
                raise  # Re-raise the exception if the max attempts are exceeded

def get_the_hiring_infos(driver):
    try:
        hiring_team_name_xpath = '//div[contains(@class,"hirer-card__hirer-information")]//span[contains(@class,"jobs-poster__name")]/strong'
        hirer_job_title_xpath = '//div[contains(@class,"hirer-card__hirer-information")]//div[contains(@class,"hirer-job-title")]'

        hiring_team_name = find_element_with_retry(driver, hiring_team_name_xpath)
        hirer_job_title = find_element_with_retry(driver, hirer_job_title_xpath)

        # Create a JSON object
        hiring_info_json = {
            "hiring_team_name": hiring_team_name if hiring_team_name else "Not Available",
            "hirer_job_title": hirer_job_title if hirer_job_title else "Not Available"
        }

        # Convert the JSON object to a JSON-formatted string
        return json.dumps(hiring_info_json)

    except NoSuchElementException:
        # Return a JSON string indicating that no hiring information was found
        return json.dumps({"error": "No hiring information found"})
    except TimeoutException:
        # Handle cases where elements cannot be found within the timeout period
        return json.dumps({"error": "Timeout No hiring information found"})

def get_jobID(driver):
    from urllib.parse import urlparse, parse_qs

    # Get the current URL
    current_url = driver.current_url
    # Parse the URL using urlparse
    parsed_url = urlparse(current_url)
    # Get the query parameters
    query_params = parse_qs(parsed_url.query)
    # Access a specific parameter value
    param_value = query_params.get("currentJobId", [""])[0]
    return param_value

def get_job_details(driver):
        job_insights = {
            "jobID": "",
            "remote_status": "",
            "job_type": "",
            "company_size": "",
            "sector": "",
            "skills": "",
            "stats": "",
            "scrapping_date": "",
            "Other": ""
        }
        today_date = datetime.now().strftime("%Y-%m-%d")
        job_insights["scrapping_date"] = str(today_date)
        job_insights["jobID"] = get_jobID(driver)

        try :
            wait = WebDriverWait(driver, 120)
            stat_element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                      "//div[contains(@class, 'job-details-jobs-unified-top-card__primary-description-without-tagline')]")))
            stat_date_nm_of_application = stat_element.text
            job_insights["stats"] = str(stat_date_nm_of_application)
        except (NoSuchElementException, StaleElementReferenceException):
            return json.dumps({"error": "Some elements were not found or were stale. Proceeding with available data."})


        try:
            insights_container = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.mt2.mb2 > ul"))
            )
            insights_elements = insights_container.find_elements(By.CSS_SELECTOR,
                                                                 "li.job-details-jobs-unified-top-card__job-insight")
            time.sleep(5)

            for insight in insights_elements:
                text = insight.text.strip()
                if "employees" in text:
                    parts = text.split('·')
                    job_insights["company_size"] = parts[0].strip() if len(parts) > 0 else ""
                    job_insights["sector"] = parts[1].strip() if len(parts) > 1 else ""
                elif "Skills:" in text:
                    job_insights["skills"] = text.replace("Skills:", "").strip()
                else:
                    spans = insight.find_elements(By.CSS_SELECTOR, "span")
                    for span in spans:
                        span_text = span.text.strip()
                        if span_text:
                            if span_text in ["Remote", "On-site","Hybrid"]:
                                job_insights["remote_status"] = span_text
                            elif "time" in span_text:
                                job_insights["job_type"] = span_text
                            else:
                                job_insights["Other"] = span_text
        except (NoSuchElementException, StaleElementReferenceException):
            return json.dumps({"error2": "Some elements were not found or were stale. Proceeding with available data."})
        return json.dumps(job_insights)

def get_job_skills_json(driver):
    # XPath to find the <a> element containing the skills
    xpath_skills = "//div[contains(@class, 'job-details-how-you-match__skills-item-wrapper')]//a[contains(@class, 'job-details-how-you-match__skills-item-subtitle')]"

    try:
        # Use the XPath to find the element containing the skills text
        skills_element = driver.find_element(By.XPATH, xpath_skills)
        skills_text = skills_element.text.strip()

        # The skills are listed in a comma-separated string, so split them into a list
        skills_list = [skill.strip() for skill in skills_text.split(',')]

        # Create a dictionary to hold the skills
        skills_dict = {
            "skills": skills_list
        }

        # Convert the dictionary to a JSON-formatted string
        skills_json = json.dumps(skills_dict)

        return skills_json

    except (NoSuchElementException, StaleElementReferenceException):
# Return an empty JSON string if the skills element is not found
        return json.dumps({"skills": []})

def get_specific_job_description_json(driver):
    # Construct an XPath that targets the specific job description
    try : 
        xpath = "//article[contains(@class,'jobs-description__container')]//div[contains(@class,'jobs-description__content')]//div[@id='job-details']"
    
        # Use the constructed XPath to find the element
        description_element = driver.find_element(By.XPATH, xpath)
    
        # Retrieve the text content of the job description
        job_description = description_element.text.strip()
    
        # Create a dictionary to hold the job description
        job_description_dict = {
            "job_description": job_description
        }
    
        # Convert the dictionary to a JSON-formatted string
        job_description_json = json.dumps(job_description_dict)
        return job_description_json

    except (NoSuchElementException, StaleElementReferenceException):
        return json.dumps({"error": "Some elements were not found or were stale. Proceeding with available data."})



def get_job_elements(job):
    try:
        # Check if the job elements are present on the page
        job_title_element = job.find_element(By.XPATH, './/a[contains(@class, "job-card-list__title")]')
        company_name_element = job.find_element(By.XPATH, './/span[contains(@class, "job-card-container__primary-description")]')
        location_element = job.find_element(By.XPATH, './/li[contains(@class, "job-card-container__metadata-item")]')

        job_title = job_title_element.text.strip()
        company_name = company_name_element.text.strip()
        location = location_element.text.strip()

        try:
            promoted_element = job.find_element(By.CLASS_NAME, 'job-card-container__footer-item')
            is_promoted = "Promoted" in promoted_element.text.strip()
            promoted_status = "Promoted" if is_promoted else "Not Promoted"
        except NoSuchElementException:
            promoted_status = "Not Promoted"

        try:
            easy_apply_element = job.find_element(By.XPATH, './/li[contains(@class, "job-card-container__apply-method")]')
            easy_apply_status = "Easy Apply" if "Easy Apply" in easy_apply_element.text.strip() else "Not Easy Apply"
        except NoSuchElementException:
            easy_apply_status = "Not Easy Apply"

        job_details = {
            "job_title": job_title,
            "company_name": company_name,
            "location": location,
            "promoted_status": promoted_status,
            "easy_apply_status": easy_apply_status
        }

        # Convert the dictionary to a JSON-formatted string
        return json.dumps(job_details)

    except (NoSuchElementException, StaleElementReferenceException):
        # If the elements are not found, handle the situation accordingly
        print("Job elements not found. Skipping job.")
        return None


def get_jobs_no_pages(driver):
    job_card_containers = driver.find_elements(By.XPATH,
                                               "//div[@class='job-card-container']")

    # Extract and print the titles
    for job_card_container in job_card_containers:
        title_element = job_card_container.find_element(By.CLASS_NAME, 'job-card-container__title')
        title_text = title_element.text
        print("Title:", title_text)

def is_page_scrollable(driver):
    # Check if the page is scrollable
    return driver.execute_script("return document.documentElement.scrollHeight > document.documentElement.clientHeight;")

def page_scrolling_for_elements_loading(driver):
    scrobality = is_page_scrollable(driver)

    job_listings_container = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, '//ul[contains(@class,"scaffold-layout__list-container")]')))

    job_elements = job_listings_container.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')

    first_job_element = job_elements[0]

    # Scroll to the bottom of the page to load all the listed Jobs then go back to the start
    while True:
        last_job_element = job_elements[-1]

        # Scroll the last job element into view gently
        driver.execute_script(
            "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });",
            last_job_element)

        # Wait for a short time to allow new content to load
        driver.implicitly_wait(5)

        # Check if there are more job elements to load
        new_last_job_element = job_listings_container.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')[-1]
        if last_job_element == new_last_job_element:
            break  # Exit the loop if no more content is loaded

    time.sleep(3)
    # Scroll back to the start gently
    driver.execute_script('arguments[0].scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });',
                          first_job_element)
    time.sleep(3)

def search_for_jobs(driver,name):
    # Type the job's name in the search bar
    search_input_xpath = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//input[@class='search-global-typeahead__input']"))
    )
    search_input_xpath.send_keys(name)
    search_input_xpath.send_keys(Keys.RETURN)

    # GO to the job Section
    time.sleep(5)
    jobs_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class ,"artdeco-pill") and text()="Jobs"]'))
    )
    jobs_button.click()
    time.sleep(10)


def check_for_no_job_matches(driver):
    # XPath to find any <h1> elements that contain the specific no job match text
    xpath_no_jobs = "//h1[contains(text(), 'No matching jobs found for')]"

    # Try to find the "No matching jobs found" message using the XPath
    no_jobs_elements = driver.find_elements(By.XPATH, xpath_no_jobs)

    # If such elements are found, it means no job matches are present on the page
    if 'No matching' in no_jobs_elements:
        print("No matching jobs found.")
        return None
    else:
        print("Job matches found.")
        return True



def job_extract(driver, name):
    hdfs_client = InsecureClient('hdfs://localhost:9870', user='aa')
    search_for_jobs(driver, name)
    all_jobs = []  # Initialize an empty list to hold all job details

    # Start with the first page
    current_page_index = 0
    job_checker = check_for_no_job_matches(driver)
    if job_checker:
        try:
            while True:
                print(f"Current Page Index: {current_page_index}")

                # Get the current page details
                current_pages = get_page_details(driver)

                # Click on the current page
                if current_pages:
                    if current_page_index < len(current_pages):
                        # Click on the current page
                        if current_page_index == 0 :
                            page = current_pages[current_page_index]
                            page.click()
                            time.sleep(5)

                            # Page scrolling in order to load all elements
                            page_scrolling_for_elements_loading(driver)

                            job_elements = get_job_containers_in_page(driver)

                            for job in job_elements:
                                # Skip the "Recommended for you" section
                                time.sleep(3)
                                try:
                                    job.click()
                                    job_data = {}
                                    job_data['details'] = get_job_elements(job)
                                    job_data['hirer_infos'] = get_the_hiring_infos(driver)
                                    job_data['job_insights'] = get_job_details(driver)
                                    job_data['specific_description'] = get_specific_job_description_json(driver)
                                    job_data['skills'] = get_job_skills_json(driver)
                                    print(job_data)
                                    all_jobs.append(job_data)

                                except Exception as e:
                                    print(f"Error while processing job: {e}")
                                    continue  # Continue to the next job element even if an exception occurs
                            current_page_index += 1

                        else:
                            print("No more pages to click.")
                            break

                    else:
                        page_scrolling_for_elements_loading(driver)
                        job_elements = get_job_containers_in_page(driver)

                        if not job_elements:
                            print("No job elements found.")
                            break

                        for job in job_elements:
                            job.click()
                            job_data = {}
                            job_data['details'] = get_job_elements(job)
                            job_data['hirer_infos'] = get_the_hiring_infos(driver)
                            job_data['job_insights'] = get_job_details(driver)
                            job_data['specific_description'] = get_specific_job_description_json(driver)
                            job_data['skills'] = get_job_skills_json(driver)
                            print(job_data)
                            all_jobs.append(job_data)
                        print('done')
                        break

                time.sleep(2)
                # Move to the next page
            print('Exited ?')
        finally:
            # Ensure the driver quits even if there's an error
            driver.quit()

    # Convert the list of job details to a JSON string
    jobs_json = json.dumps(all_jobs, indent=4)
    file_path = '/home/aa/PycharmProjects/Linkedin/junk/jobs_data.json'  # For example, saving in the 'data' directory of this environment

    # Writing the JSON string to a file
    with open(file_path, 'w') as file:
        file.write(jobs_json)

    print(f'File saved successfully at {file_path}')
    # Here you can return the JSON string, print it, or write it to a file
    return jobs_json

