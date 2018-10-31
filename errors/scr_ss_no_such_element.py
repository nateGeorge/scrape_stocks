nothing to scrape right now
---------------------------------------------------------------------------
NoSuchElementException                    Traceback (most recent call last)
~/github/scrape_stocks/scrape_shortsqueeze.py in <module>()
    321     driver = log_in(driver)
    322     time.sleep(3)  # wait for login to complete...could also use some element detection
--> 323     daily_updater(driver)

~/github/scrape_stocks/scrape_shortsqueeze.py in daily_updater(driver)
    276             print('more than 1 day out of date, downloading...')
    277             download_daily_data(driver)
--> 278             check_for_new_excel(driver)
    279         elif (latest_close_date.date() - latest_scrape) == pd.Timedelta('1D'):
    280             if today_utc.hour > latest_close_date.hour:

~/github/scrape_stocks/scrape_shortsqueeze.py in check_for_new_excel(driver)
     90     """
     91     driver.get('http://shortsqueeze.com/ShortFiles.php')
---> 92     years = get_years(driver)
     93     # get currently downloaded files
     94     dates_df = pd.read_excel(HOME_DIR + 'short_squeeze_release_dates.xlsx', None)

~/github/scrape_stocks/scrape_shortsqueeze.py in get_years(driver)
     52     gets available years from the title bar
     53     """
---> 54     menu_bar = driver.find_element_by_xpath('/html/body/div/table[9]/tbody/tr/td/div/table')
     55     years = menu_bar.text.split('\n')
     56     int_years = []

/usr/local/lib/python3.5/dist-packages/selenium/webdriver/remote/webdriver.py in find_element_by_xpath(se$f, xpath)
    363             driver.find_element_by_xpath('//div/td[1]')
    364         """
--> 365         return self.find_element(by=By.XPATH, value=xpath)
    366
    367     def find_elements_by_xpath(self, xpath):

/usr/local/lib/python3.5/dist-packages/selenium/webdriver/remote/webdriver.py in find_element(self, by, va
lue)
    841         return self.execute(Command.FIND_ELEMENT, {
    842             'using': by,
--> 843             'value': value})['value']
    844
    845     def find_elements(self, by=By.ID, value=None):

/usr/local/lib/python3.5/dist-packages/selenium/webdriver/remote/webdriver.py in execute(self, driver_comm
and, params)
    306         response = self.command_executor.execute(driver_command, params)
    307         if response:
--> 308             self.error_handler.check_response(response)
    309             response['value'] = self._unwrap_value(
    310                 response.get('value', None))

    /usr/local/lib/python3.5/dist-packages/selenium/webdriver/remote/errorhandler.py in check_response(self, response)
    192         elif exception_class == UnexpectedAlertPresentException and 'alert' in value:
    193             raise exception_class(message, screen, stacktrace, value['alert'].get('text'))
--> 194         raise exception_class(message, screen, stacktrace)
    195
    196     def _value_or_default(self, obj, key, default):

NoSuchElementException: Message: Unable to locate element: /html/body/div/table[9]/tbody/tr/td/div/table
