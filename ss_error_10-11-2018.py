more than 1 day out of date, downloading...
---------------------------------------------------------------------------
WebDriverException                        Traceback (most recent call last)
~/github/scrape_stocks/scrape_shortsqueeze.py in <module>
    358     display.start()
    359
--> 360     daily_updater()

~/github/scrape_stocks/scrape_shortsqueeze.py in daily_updater()
    295             print('more than 1 day out of date, downloading...')
    296             driver = setup_driver()
--> 297             driver = log_in(driver)
    298             time.sleep(3)  # wait for login to complete...could also use some
element detection
    299             download_daily_data(driver)

~/github/scrape_stocks/scrape_shortsqueeze.py in log_in(driver)
    333     while True:
    334         try:
--> 335             driver.get(login_url)
    336             time.sleep(1 + np.random.rand())  # should add WebDriverWait
    337             username = driver.find_element_by_xpath('/html/body/div/table[5]/$
body/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input')

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in get($
elf, url)
    322         Loads a web page in the current browser session.
    323         """
--> 324         self.execute(Command.GET, {'url': url})
    325
    326     @property

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/webdriver.py in exec$
te(self, driver_command, params)
    310         response = self.command_executor.execute(driver_command, params)
    311         if response:
--> 312             self.error_handler.check_response(response)
    313             response['value'] = self._unwrap_value(
    314                 response.get('value', None))

/usr/local/lib/python3.6/dist-packages/selenium/webdriver/remote/errorhandler.py in ch
eck_response(self, response)
    240                 alert_text = value['alert'].get('text')
    241             raise exception_class(message, screen, stacktrace, alert_text)
--> 242         raise exception_class(message, screen, stacktrace)
    243
    244     def _value_or_default(self, obj, key, default):

WebDriverException: Message: Reached error page: about:neterror?e=dnsNotFound&u=http%3
A//shortsqueeze.com/signin.php&c=UTF-8&f=regular&d=We%20can%E2%80%99t%20connect%20to%2
0the%20server%20at%20shortsqueeze.com.
