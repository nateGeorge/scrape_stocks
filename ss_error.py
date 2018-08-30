no new files to download
sleeping 1h...
---------------------------------------------------------------------------
NoSuchElementException                    Traceback (most recent call last)
~/github/scrape_stocks/scrape_shortsqueeze.py in daily_updater(driver)
    307         try:
--> 308             driver = log_in(driver)
    309         except NoSuchElementException:

~/github/scrape_stocks/scrape_shortsqueeze.py in log_in(driver)
    320             time.sleep(1 + np.random.rand())  # should add WebDriverWait
--> 321             username = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/tabl
e/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input')
    322             password = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/tabl
e/tbody/tr/td/form/table/tbody/tr[2]/td[2]/input')

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in find_element_by_xpath(se
lf, xpath)
    384         """
--> 385         return self.find_element(by=By.XPATH, value=xpath)
    386

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in find_element(self, by, v
alue)
    954             'using': by,
--> 955             'value': value})['value']
    956

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in execute(self, driver_com
mand, params)
    311         if response:
--> 312             self.error_handler.check_response(response)
    313             response['value'] = self._unwrap_value(

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/errorhandler.py in check_response(self,
response)
    241             raise exception_class(message, screen, stacktrace, alert_text)
--> 242         raise exception_class(message, screen, stacktrace)
    243

NoSuchElementException: Message: Unable to locate element: /html/body/div/table[5]/tbody/tr/td/div/table/
tbody/tr/td/form/table/tbody/tr[1]/td[2]/input


During handling of the above exception, another exception occurred:

NoSuchElementException                    Traceback (most recent call last)
~/github/scrape_stocks/scrape_shortsqueeze.py in <module>()
    344     driver = log_in(driver)
    345     time.sleep(3)  # wait for login to complete...could also use some element detection
--> 346     daily_updater(driver)

~/github/scrape_stocks/scrape_shortsqueeze.py in daily_updater(driver)
    310             driver.quit()
    311             driver = setup_driver()
--> 312             driver = log_in(driver)
    313         time.sleep(3)
    314

~/github/scrape_stocks/scrape_shortsqueeze.py in log_in(driver)
    319             driver.get(login_url)
    320             time.sleep(1 + np.random.rand())  # should add WebDriverWait
--> 321             username = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/tabl
e/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input')
    322             password = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/tabl
e/tbody/tr/td/form/table/tbody/tr[2]/td[2]/input')
    323             username.send_keys(UNAME)

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in find_element_by_xpath(se
lf, xpath)
    383             element = driver.find_element_by_xpath('//div/td[1]')
    384         """
--> 385         return self.find_element(by=By.XPATH, value=xpath)
    386
    387     def find_elements_by_xpath(self, xpath):

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in find_element(self, by, v
alue)
    953         return self.execute(Command.FIND_ELEMENT, {
    954             'using': by,
--> 955             'value': value})['value']
    956
    957     def find_elements(self, by=By.ID, value=None):

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in execute(self, driver_com
mand, params)
    310         response = self.command_executor.execute(driver_command, params)
    311         if response:
--> 312             self.error_handler.check_response(response)
    313             response['value'] = self._unwrap_value(
    314                 response.get('value', None))

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/errorhandler.py in check_response(self,
response)
    240                 alert_text = value['alert'].get('text')
    241             raise exception_class(message, screen, stacktrace, alert_text)
--> 242         raise exception_class(message, screen, stacktrace)
    243
    244     def _value_or_default(self, obj, key, default):

NoSuchElementException: Message: Unable to locate element: /html/body/div/table[5]/tbody/tr/td/div/table/
tbody/tr/td/form/table/tbody/tr[1]/td[2]/input
