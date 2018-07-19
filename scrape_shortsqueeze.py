# TODO: dynamically update HOME_DIR + 'short_squeeze_release_dates.xlsx'

# would need to use selenium to get this to work...meh, just use a multidownloader for chrome
# core
import os
import time
import pytz
import glob
import calendar
import datetime

# installed
import requests as req
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

# custom
import scrape_stockdata as ss
from utils import get_home_dir

# for headless browser mode with FF
# http://scraping.pro/use-headless-firefox-scraping-linux/
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()


try:
    ua = UserAgent()
except:
    print("Couldn't make user agent, trying again")
    ua = UserAgent()

base_url = 'http://shortsqueeze.com/{}.php'
login_url = 'http://shortsqueeze.com/signin.php'
daily_url = 'http://shortsqueeze.com/down.php?fi={}.csv'  # date should be like 2017-11-13

YEARS = ['2015', '2016', '2017']
UNAME = os.environ.get('ss_uname')
PWORD = os.environ.get('ss_pass')
HOME_DIR = get_home_dir(repo_name='scrape_stocks')


def get_years(driver):
    """
    gets available years from the title bar
    """
    menu_bar = driver.find_element_by_xpath('/html/body/div/table[9]/tbody/tr/td/div/table')
    years = menu_bar.text.split('\n')
    int_years = []
    for y in years:
        try:
            int_years.append(int(y))
        except ValueError:
            pass

    return np.array(int_years)


def parse_bimo_dates(filename, dates_df, rev_cal_dict):
    """
    gets date from release dates dataframe and filename
    """
    # get the date from the dates_df and filename
    # old way of doing it which worked before the effed up filenames with an extra 0 in nov 2017...
    # date = f.split('/')[-1][9:16]
    date = filename.split('/')[-1].split('-')[0].split('.')[1]
    year = date[:4]
    month_num = int(date[-3:-1])
    month = rev_cal_dict[month_num]
    ab = date[-1].upper()
    t_df = dates_df[year]
    date = '-'.join([year,
                    str(month_num).zfill(2),
                    str(t_df[t_df[int(year)] == (month + ' ' + ab)]['NASDAQ®'].values[0]).zfill(2)])
    date = pd.to_datetime(date, format='%Y-%m-%d')
    return date


def check_for_new_excel(driver):
    """
    checks for new excel files to download, and if they aren't in the data folder,
    downloads them
    """
    driver.get('http://shortsqueeze.com/ShortFiles.php')
    years = get_years(driver)
    # get currently downloaded files
    dates_df = pd.read_excel(HOME_DIR + 'short_squeeze_release_dates.xlsx', None)
    cal_dict = {v: k for k, v in enumerate(calendar.month_name)}
    del cal_dict['']
    rev_cal_dict = {v: k for k, v in cal_dict.items()}

    bimonthly_files = glob.glob(HOME_DIR + 'data/short_squeeze.com/*.xlsx')
    bimonthly_filenames = set([f.split('/')[-1] for f in bimonthly_files])
    bimo_dates = [parse_bimo_dates(f, dates_df, rev_cal_dict) for f in bimonthly_files]
    latest_date = max(bimo_dates).date()
    latest_year = latest_date.year
    check_years = years[years >= latest_year]

    files_to_dl = []
    filenames = []
    for y in check_years:
        driver.get('http://shortsqueeze.com/' + str(y) + '.php')
        links = driver.find_elements_by_partial_link_text('Download')
        for l in links:
            link = l.get_attribute('href')
            if link == 'http://shortsqueeze.com/ShortFiles.php':
                continue

            filename = link.split('/')[-1]
            if filename in bimonthly_filenames:
                continue

            files_to_dl.append(link)
            filenames.append(filename)

    if len(files_to_dl) == 0:
        print('no new files to download')

    # seems to hang on download, so this will make it continue
    driver.set_page_load_timeout(4)
    for l in files_to_dl:
        try:
            print('downloading', l)
            driver.get(l) # saves to downloads folder
        except TimeoutException:
            pass

    for f in filenames:
        full_fn = '/home/nate/Downloads/' + f
        print(full_fn)
        if os.path.exists(full_fn):
            os.rename(full_fn, HOME_DIR + 'data/short_squeeze.com/' + f)


def setup_driver(backend='FF'):
    """
    :param backend: string, one of FF, PH, CH (firefox, phantom, or chrome)
    currently phantomjs cannot download files
    """
    if backend == 'PH':
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
            "(KHTML, like Gecko) Chrome/15.0.87"
        )
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(1920, 1080)
    elif backend == 'FF':
        # couldn't get download working without manual settings...
        # https://stackoverflow.com/questions/38307446/selenium-browser-helperapps-neverask-openfile-and-savetodisk-is-not-working
        # create the profile (on ubuntu, firefox -P from command line),
        # download once, check 'don't ask again' and 'save'
        # also change downloads folder to ticker_data within git repo
        # then file path to profile, and use here:
        prof_path = '/home/nate/.mozilla/firefox/4mmudyyu.short_squeeze' # short_squeeze was the name of the profile
        # saves to downloads folder by default
        profile = webdriver.FirefoxProfile(prof_path)
        # auto-download unknown mime types:
        # http://forums.mozillazine.org/viewtopic.php?f=38&t=2430485
        # set to text/csv and comma-separated any other file types
        # https://stackoverflow.com/a/9329022/4549682
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        # https://www.lifewire.com/firefox-about-config-entry-browser-445707
        # profile.set_preference('browser.download.folderList', 1) # downloads folder
        # profile.set_preference('browser.download.manager.showWhenStarting', False)
        # profile.set_preference('browser.helperApps.alwaysAsk.force', False)
        # # profile.set_preference('browser.download.dir', '/tmp')
        # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', '*')
        driver = webdriver.Firefox(profile, executable_path='/home/nate/geckodriver')
    elif backend == 'CH':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
          "download.default_directory": '/home/nate/Downloads/',
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True
        })
        driver = webdriver.Chrome(chrome_options=options, executable_path='/home/nate/geckodriver')

    return driver


def get_latest_daily_date():
    # get latest date from daily scrapes
    daily_files = glob.glob(HOME_DIR + 'data/short_squeeze_daily/*.csv')
    daily_dates = [pd.to_datetime(f.split('/')[-1].split('.')[0]) for f in daily_files]
    last_daily = max(daily_dates).date()
    return last_daily


def download_daily_data(driver=None, date=None):
    """
    checks which files already exist, then downloads remaining files to bring up to current

    or if 'date' supplied (i.e. 2018-04-12, yyyy-mm-dd, as a string), then downloads for that specific date
    """
    if driver is None:
        driver = setup_driver()
        driver = log_in(driver)
        time.sleep(3)  # wait for login to complete...could also use some element detection

    # TODO: check which files are missing or are size 0 in the existing files after the latest
    # excel file, and download those.  delete/archive any files older than the last excel file
    last_daily = get_latest_daily_date()
    today_utc = pd.to_datetime('now')
    # was thinking about using NY time, but mcal is in UTC
    # local_tz = pytz.timezone('America/New_York')
    # today_ny = today_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
    ndq = mcal.get_calendar('NASDAQ')
    open_days = ndq.schedule(start_date=today_utc - pd.Timedelta(str(3*365) + ' days'), end_date=today_utc)
    # basically, this waits for 3 hours after market close if it's the same day
    if open_days.iloc[-1]['market_close'].date() == today_utc.date():
        open_days = open_days.iloc[:-1]

    open_dates = np.array([o['market_close'].date() for l, o in open_days.iterrows()])
    if date is None:
        to_scrape = open_dates[open_dates > last_daily]
        if len(to_scrape) == 0:
            print('nothing to scrape right now')
            return
    else:
        date_strptime = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if date_strptime not in open_dates:
            print('supplied date of', date, 'is not in the open_dates, doing nothing...')
            return
        else:
            to_scrape = [date_strptime]

    # seems to hang on download, so this will make it continue
    driver.set_page_load_timeout(4)
    filenames = []
    for s in to_scrape:
        d = s.strftime('%Y-%m-%d')
        url = daily_url.format(d)
        filename = url.split('=')[-1]  # gets csv filename right now
        filenames.append(filename)
        try:
            print('downloading', filename)
            driver.get(url) # saves to downloads folder
        except TimeoutException:
            pass

    # moves file to data folder
    for f in filenames:
        og_file = '/home/nate/Downloads/' + f
        if os.path.exists(og_file):
            os.rename(og_file, HOME_DIR + 'data/short_squeeze_daily/' + f)


def check_market_status():
    """
    Checks to see if market is open today.
    Uses the pandas_market_calendars package as mcal
    """
    # today = datetime.datetime.now(pytz.timezone('America/New_York')).date()
    today_utc = pd.to_datetime('now').date()
    ndq = mcal.get_calendar('NASDAQ')
    open_days = ndq.schedule(start_date=today_utc - pd.Timedelta('10 days'), end_date=today_utc)
    if today_utc in open_days.index:
        return open_days
    else:
        return None


def get_latest_close_date(market='NASDAQ'):
    """
    gets the latest date the markets were open (NASDAQ), and returns the closing datetime
    """
    # today = datetime.datetime.now(pytz.timezone('America/New_York')).date()
    today_utc = pd.to_datetime('now').date()
    ndq = mcal.get_calendar(market)
    open_days = ndq.schedule(start_date=today_utc - pd.Timedelta('10 days'), end_date=today_utc)
    return open_days.iloc[-1]['market_close']


def daily_updater(driver):
    """
    checks if any new files to download, if so, downloads them
    """
    latest_scrape = get_latest_daily_date()
    while True:
        latest_close_date = get_latest_close_date()
        today_utc = pd.to_datetime('now')
        today_ny = datetime.datetime.now(pytz.timezone('America/New_York'))
        pd_today_ny = pd.to_datetime(today_ny.date())
        if (latest_close_date.date() - latest_scrape) > pd.Timedelta('1D'):
            print('more than 1 day out of date, downloading...')
            download_daily_data(driver)
            check_for_new_excel(driver)
        elif (latest_close_date.date() - latest_scrape) == pd.Timedelta('1D'):
            if today_utc.hour > latest_close_date.hour:
                print('market closed, checking for new data...')
                download_daily_data(driver)
                check_for_new_excel(driver)
        elif pd_today_ny.date() == latest_close_date.date():  # if the market is open and the db isn't up to date with today...
            if today_ny.hour >= 22:
                print('downloading update from today...')
                download_daily_data(driver)
                check_for_new_excel(driver)

        print('sleeping 1h...')
        time.sleep(3600)
        # need to login again because it will have logged out by then
        driver.quit()
        driver = setup_driver()
        driver = log_in(driver)
        time.sleep(3)


def log_in(driver):
    while True:
        try:
            driver.get(login_url)
            time.sleep(1 + np.random.rand())  # should add WebDriverWait
            username = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input')
            password = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/input')
            username.send_keys(UNAME)
            password.send_keys(PWORD)
            time.sleep(1 + np.random.rand())
            signIn = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input')
            signIn.click()
            return driver
            break  # not sure if this necessary, but just in case
        except TimeoutException:
            driver.quit()
            driver = setup_driver()



if __name__ == "__main__":
    driver = setup_driver()
    driver = log_in(driver)
    time.sleep(3)  # wait for login to complete...could also use some element detection
    daily_updater(driver)
