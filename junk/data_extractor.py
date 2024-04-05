from customer_chrome_driver import CustomChromeDriver

class DataExtractor:
    def __init__(self, custom_driver):
        self.custom_driver = custom_driver

    def extract_data_from_linkedin(self):
        self.custom_driver.navigate_to_url('https://linkedin.com')
        print("Data extraction from LinkedIn completed.")

    # Add more methods for different extraction tasks

# Example usage:
custom_driver = CustomChromeDriver()
data_extractor = DataExtractor(custom_driver)
data_extractor.extract_data_from_linkedin()