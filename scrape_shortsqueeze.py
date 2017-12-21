# would need to use selenium to get this to work...meh, just use a multidownloader for chrome
# core
import os
import time
import pytz
import glob
import shutil

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

def scrape_stuff():
    # abandoned function after using chrome multidownloader
    for y in YEARS:
        url = base_url.format(y)
        res = req.get(url)
        soup = bs(res.content, 'lxml')
        soup.find_all({'class': 'hyper13'})


def get_years():
    """
    gets available years from the title bar
    """


def check_for_new_excel():
    """
    checks for new excel files to download, and if they aren't in the data folder,
    downloads them
    """


def download_new_excel():
    if check_for_new_excel():
        # download file here
        pass

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
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
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


def download_daily_data(driver):
    """
    checks which files already exist, then downloads remaining files to bring up to current
    """
    # get latest date from daily scrapes
    daily_files = glob.glob(HOME_DIR + 'data/short_squeeze_daily/*.csv')
    daily_dates = [pd.to_datetime(f.split('/')[-1].split('.')[0]) for f in daily_files]
    last_daily = max(daily_dates).date() # pytz.utc.localize(

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
    to_scrape = open_dates[open_dates > last_daily]
    if len(to_scrape) == 0:
        print('nothing to scrape right now')
        return

    # seems to hang on download, so this will make it continue
    driver.set_page_load_timeout(4)

    # TODO: set download directory somehow, or use another profile
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


def log_in(driver):
    driver.get(login_url)
    time.sleep(1 + np.random.rand())  # should add WebDriverWait
    username = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input')
    password = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/input')
    username.send_keys(UNAME)
    password.send_keys(PWORD)
    time.sleep(1 + np.random.rand())
    signIn = driver.find_element_by_xpath('/html/body/div/table[5]/tbody/tr/td/div/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input')
    signIn.click()


if __name__ == "__main__":
    driver = setup_driver()
    log_in(driver)
    time.sleep(5)  # wait for login to complete...could also use some element detection
