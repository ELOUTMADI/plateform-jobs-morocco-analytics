import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


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
    job_listings_container = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,'//ul[contains(@class,"scaffold-layout__list-container")]')))
    job_elements = job_listings_container.find_elements(By.XPATH, '//div[contains(@class,"job-card-container--clickable")]')
    return job_elements

def get_job_details(driver):
    job_details_wrapper_xpath = '//div[@class="jobs-search__job-details--wrapper"]'
    job_details_wrapper = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.XPATH, job_details_wrapper_xpath))
    )

    # Extract details from the job_details_wrapper element
    job_title = job_details_wrapper.find_element(By.XPATH, '//h2[contains(@class,"job-title")]').text
    location_element = job_details_wrapper.find_element(By.XPATH,
                                                './/li[contains(@class, "job-card-container__metadata-item")]').text


    return job_title

def get_job_elements(job):
    try :
        job_title_element = job.find_element(By.XPATH, './/a[contains(@class, "job-card-list__title")]')
        company_name_element = job.find_element(By.XPATH,
                                                        './/span[contains(@class, "job-card-container__primary-description")]')
        location_element = job.find_element(By.XPATH,
                                                    './/li[contains(@class, "job-card-container__metadata-item")]')


        job_title = job_title_element.text.strip()
        company_name = company_name_element.text.strip()
        location = location_element.text.strip()
    except NoSuchElementException:
        print("Element not found, skipping job.")
        return None

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

    return [job_title,company_name,location,promoted_status,easy_apply_status]

def get_jobs_no_pages(job):
    try:
        job_details_wrapper_xpath = '//div[@class="jobs-search__job-details--wrapper"]'
        job_details_wrapper = WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.XPATH, job_details_wrapper_xpath))
        )

        # Extract details from the job_details_wrapper element
        job_title = job_details_wrapper.find_element(By.XPATH, '//h2[contains(@class,"job-title")]').text
        about_company_name_element = job.find_element(By.XPATH,
                                                './/div[contains(@class, "primary-description-container")]').text

    except NoSuchElementException:
        print("Element not found, skipping job.")
        return None

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

    return [job_title, about_company_name_element, promoted_status, easy_apply_status]
def page_scrolling_for_elements_loading(driver):
    job_listings_container = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, '//ul[contains(@class,"scaffold-layout__list-container")]')))

    first_job_element = job_listings_container.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')[0]

    # Scroll to the bottom of the page to load all the listed Jobs then go back to the start
    while True:
        last_job_element = job_listings_container.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')[-1]

        # Scroll the last job element into view gently
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });", last_job_element)

        # Wait for a short time to allow new content to load
        driver.implicitly_wait(5)

        # Check if there are more job elements to load
        new_last_job_element = job_listings_container.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')[-1]
        if last_job_element == new_last_job_element:
            break  # Exit the loop if no more content is loaded

    time.sleep(3)
    # Scroll back to the start gently
    driver.execute_script('arguments[0].scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });', first_job_element)
    time.sleep(3)

def job_extract(driver, name):
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

    # Get all Job listing
    time.sleep(10)

    # Start with the first page
    current_page_index = 0

    while True:

        # Get the current page details
        current_pages = get_page_details(driver)

        # Click on the current page
        if current_pages and current_page_index < len(current_pages):
            # Click on the current page
            page = current_pages[current_page_index]
            page.click()
            time.sleep(5)

            # Page scrolling in order to load all elements
            page_scrolling_for_elements_loading(driver)

            job_elements = get_job_containers_in_page(driver)

            for job in job_elements:
                time.sleep(3)
                job.click()
                # details = get_job_details(driver)
                details = get_job_elements(job)
                print(f'About the Job: {details}')
        else:
            page_scrolling_for_elements_loading(driver)
            job_elements = get_job_containers_in_page(driver)

            for job in job_elements:
                time.sleep(3)
                job.click()
                # details = get_job_details(driver)
                details = get_jobs_no_pages(job)
                print(f'About the Job: {details}')
        # Wait for some time (adjust as needed)
        time.sleep(2)

        # Move to the next page
        current_page_index += 1

    input('what ?')



if __name__ == "__main__":
    driver = uc.Chrome()
    logged_in_driver = login(driver)
    job_extract(logged_in_driver, 'data science healthcare')