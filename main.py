from data_extraction.data_extraction import *
from data_ingestion.data_lake import *

if __name__ == "__main__":
    job_name = 'Health Care Research Pharmacy'
    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    # Clear local storage via JavaScript
    driver.execute_script("window.localStorage.clear();")
    logged_in_driver = login(driver)
    jobs_json = job_extract(logged_in_driver, job_name)
    print(jobs_json)
    hdfs_client = InsecureClient('http://localhost:9870/', user='hdoop')
    jobs_json = json.dumps(jobs_json, indent=4)
    save_to_hdfs(hdfs_client, job_name.replace(" ", "_").lower(),jobs_json)
