import undetected_chromedriver as uc

class CustomChromeDriver:
    def __init__(self):
        self.chrome_options = uc.ChromeOptions()
        self.chrome_options.add_argument('--ignore-certificate-errors')

        self.driver = uc.Chrome(options=self.chrome_options)

    def set_language(self, language_code):
        self.chrome_options.add_argument(f'--lang={language_code}')

    def set_timezone(self, timezone):
        self.chrome_options.add_argument(f'--timezone={timezone}')

    def set_geolocation(self, latitude, longitude, accuracy):
        self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy
        })
    def navigate_to_url(self, url):
        self.driver.get(url)

    def observe_webpage(self):
        input("Press Enter after observing the webpage...")

    def close_browser(self):
        self.driver.quit()


custom_driver = CustomChromeDriver()
custom_driver.set_language('en')
custom_driver.set_timezone('America/Los_Angeles')
custom_driver.set_geolocation(37.7749, -122.4194, 100)
custom_driver.navigate_to_url('https://linkedin.com')
custom_driver.observe_webpage()
