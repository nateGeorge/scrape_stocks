no new files to download
sleeping 1h...
---------------------------------------------------------------------------
NoSuchElementException                    Traceback (most recent call last)
~/github/scrape_stocks/scrape_shortsqueeze.py in <module>()
    337     driver = log_in(driver)
    338     time.sleep(3)  # wait for login to complete...could also use some element detection
--> 339     daily_updater(driver)

~/github/scrape_stocks/scrape_shortsqueeze.py in daily_updater(driver)
    303         driver.quit()
    304         driver = setup_driver()
--> 305         driver = log_in(driver)
    306         time.sleep(3)
    307

~/github/scrape_stocks/scrape_shortsqueeze.py in log_in(driver)
    312             driver.get(login_url)
    313             time.sleep(1 + np.random.rand())  # should add WebDriverWait
--> 314             username = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/
table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input')
    315             password = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/
table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/input')
    316             username.send_keys(UNAME)

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in find_element_by_xpat
h(self, xpath)
    383             element = driver.find_element_by_xpath('//div/td[1]')
    384         """
--> 385         return self.find_element(by=By.XPATH, value=xpath)
    386
    387     def find_elements_by_xpath(self, xpath):

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in find_element(self, b
y, value)
    953         return self.execute(Command.FIND_ELEMENT, {
    954             'using': by,
--> 955             'value': value})['value']
    956
    957     def find_elements(self, by=By.ID, value=None):

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in execute(self, driver
_command, params)
    310         response = self.command_executor.execute(driver_command, params)
    311         if response:
--> 312             self.error_handler.check_response(response)
    313             response['value'] = self._unwrap_value(
    314                 response.get('value', None))

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/errorhandler.py in check_response(se
lf, response)
240                 alert_text = value['alert'].get('text')
241             raise exception_class(message, screen, stacktrace, alert_text)
--> 242         raise exception_class(message, screen, stacktrace)
243
244     def _value_or_default(self, obj, key, default):

NoSuchElementException: Message: Unable to locate element: /html/body/div/table[5]/tbody/tr/td/div/ta
ble/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input
