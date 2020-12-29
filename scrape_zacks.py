# core
import glob
import os
import time
import datetime
import threading
import traceback
import subprocess
from bson import json_util
# makes firefox headless: https://stackoverflow.com/a/10399597/4549682
# subprocess.Popen('Xvfb :99 -ac &', shell=True)
# subprocess.Popen('export DISPLAY=:99', shell=True)

# installed
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
import fake_useragent
import requests as req
from requests.exceptions import Timeout, SSLError
from OpenSSL.SSL import WantReadError
from bs4 import BeautifulSoup as bs
from lxml import html
import pandas as pd
import numpy as np
from pymongo import MongoClient
import odo
import pytz
from tqdm import tqdm
import pandas_market_calendars as mcal
from pymongo import MongoClient
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor


tries = 0
while True:
    tries += 1
    if tries == 10:
        break
    try:
        # normally stored in /tmp
        location = '/home/nate/fake_useragent%s.json' % fake_useragent.VERSION
        ua = UserAgent(verify_ssl=False, use_cache_server=False, path=location)
    except:
        print("Couldn't make user agent, trying again")

BASE_URL = 'https://www.zacks.com/stock/research/{}/earnings-announcements'
DB = 'zacks_data'

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
        prof_path = '/home/nate/.mozilla/firefox/jdl7io1l.scr' # scr was the name of the profile
        profile = webdriver.FirefoxProfile(prof_path)
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


if __name__ == "__main__":
    driver = setup_driver()
    driver.get(BASE_URL.format('RHT'))
