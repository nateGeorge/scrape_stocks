# core
import glob
import os


# installed
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
import requests as req
from bs4 import BeautifulSoup as bs
from lxml import html
import pandas as pd
import numpy as np
import threading


try:
    ua = UserAgent()
except:
    print("Couldn't make user agent")
    pass


BASE_URL = 'http://www.nasdaq.com/'


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
        # create the profile, download once, check 'don't ask again' and 'save'
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


def get_latest_files():
    dl_files = '/home/nate/Downloads/*.csv'
    list_of_files = glob.glob(dl_files)
    latest_files = sorted(list_of_files, key=os.path.getctime)[-3:]

    return latest_files


def get_stock_list():
    """

    """
    # really don't need to do this, can just use the pre-made url
    # left here for educational purposes
    # url = BASE_URL + 'screening/company-list.aspx'
    # res = req.get(url)
    # s = bs(res.content, 'lxml')
    # div = s.find('div', {'id': 'companyListDownloads'})
    # links = div.findall('a')
    url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&amp;exchange={}&amp;render=download'.format('nyse')
    # doesn't work because it's detecting it's a bot, even with cookies or headers

    # attempt with headers
    # import urllib.request
    # agent = ua.random  # select a random user agent
    # headers = {
    #     "Connection": "close",  # another way to cover tracks
    #     "User-Agent": agent
    # }
    # url_req = urllib.request.Request(url, headers=headers)
    # response = urllib.request.urlopen(url_req)
    # data = response.read()

    # attempt with cookies
    # driver = setup_driver()
    # cookies = driver.get_cookies()
    # sess = req.Session()
    # for cookie in cookies:
    #     session.cookies.set(cookie['name'], cookie['value'])
    #
    # res = sess.get(url)

    files = get_latest_files()  # get 3 latest files in d/l folder to check when d/ls are complete
    driver = setup_driver()
    dl_url = 'http://www.nasdaq.com/screening/company-list.aspx'
    url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&amp;exchange={}&amp;render=download'.format('nyse')
    driver.get(dl_url)
    nasdaq_list = driver.find_element_by_xpath('//*[@id="companyListDownloads"]/table/tbody/tr[1]/td[2]/a')
    nasdaq_list.click()
    nyse_list = driver.find_element_by_xpath('//*[@id="companyListDownloads"]/table/tbody/tr[2]/td[2]/a')
    nyse_list.click()
    amex_list = driver.find_element_by_xpath('//*[@id="companyListDownloads"]/table/tbody/tr[3]/td[2]/a')
    amex_list.click()

    # wait for download to finish
    latest_files = get_latest_files()
    lfs = set(latest_files)
    fs = set(files)
    while len(fs.intersection(lfs)) != 0 and len(latest_files < 3):
        time.sleep(0.5)
        latest_files = get_latest_files()

    nd = pd.read_csv(latest_files[0])
    ny = pd.read_csv(latest_files[1])
    am = pd.read_csv(latest_files[2])
    all_ex = nd.append(ny).append(am)
    all_ex.drop_duplicates(inplace=True)
    tickers = sorted(all_ex.Symbol.values)

    driver.quit()

    return tickers


def scrape_historical(t):
    """
    :param t: string, the ticker (e.g. SPY)
    """
    url = 'http://www.nasdaq.com/symbol/{}/historical'.format(t.lower())
    res = req.get(url)


def add_rows_old(el, d):
    """
    :param el: lxml element (a table)
    :param d: dictionary
    """
    soup = bs(html.tostring(el[0]), 'lxml')
    rows = soup.find_all('tr')
    for r in rows:
        cols = r.find_all('td')
        lab = cols[0].find('span').text.strip()
        val = cols[1].text.strip().strip('%')
        if val[-1] == 'k':
            val = float(val[:-1]) * 1000
        elif val[-1] == 'M':
            val = float(val[:-1]) * 1000000
        elif val[-1] == 'B':
            val = float(val[:-1]) * 1000000000
        elif val[-1] == 'T':
            val = float(val[:-1]) * 1000000000000
        elif val == 'N/A':
            val = val
        else:
            val = float(val)

        d[lab] = val

    return d


def add_rows(t, d):
    """
    :param t: a string, html table
    :param d: dictionary

    broke on BBP
    """
    rows = t.find_all('tr')
    for r in rows:
        cols = r.find_all('td')
        lab = cols[0].find('span').text.strip()

        val = cols[1].text.strip().strip('%')
        val = val.replace(',', '')
        if val[-1] == 'k':
            val = float(val[:-1]) * 1000
        elif val[-1] == 'M':
            val = float(val[:-1]) * 1000000
        elif val[-1] == 'B':
            val = float(val[:-1]) * 1000000000
        elif val[-1] == 'T':
            val = float(val[:-1]) * 1000000000000
        elif val == 'N/A':
            val = val
        else:
            try:
                val = float(val)
            except ValueError:
                pass  # if value is a date

        d[lab] = val

    return d


def scrape_stats(t):
    # broke on bbp
    # get https://finance.yahoo.com/quote/NAVI/key-statistics?p=NAVI
    url = 'https://finance.yahoo.com/quote/{0}/key-statistics?p={0}'.format(t)
    page = req.get(url)
    soup = bs(page.content, 'lxml')
    tables = soup.find_all('table')
    no_tables, no_stats = [], []
    if len(tables) == 0:
        print('WARNING: no tables found')
    elif len(tables) < 10:
        print('WARNING: no stats page for', t)

    ss_dict = {'ticker':t}
    for t in tables:
        ss_dict = add_rows(t, ss_dict)


    return pd.DataFrame(ss_dict, index=[0])


    # old way of doing it, left for educational purposes
    # should change add_rows to add_rows_old
    # tree = html.fromstring(page.content)
    # share_stats = tree.xpath('//*[@id="Col1-3-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[2]/table')
    # ss_dict = add_rows(share_stats, s_dict)
    #
    # # valuation measures section
    # val_meas = tree.xpath('//*[@id="Col1-3-KeyStatistics-Proxy"]/section/div[2]/div[1]/div[1]')
    # ss_dict = add_rows(val_meas, ss_dict)
    #
    # # profitability section
    # prof = tree.xpath('//*[@id="Col1-3-KeyStatistics-Proxy"]/section/div[2]/div[1]/div[2]/div[2]/table')
    # ss_dict = add_rows(prof, ss_dict)
    #
    # # management effectiveness section
    # man = tree.xpath('//*[@id="Col1-3-KeyStatistics-Proxy"]/section/div[2]/div[1]/div[2]/div[3]/table')
    # ss_dict = add_rows(man, ss_dict)
    #
    # # income statement
    # inc = tree.xpath('//*[@id="Col1-3-KeyStatistics-Proxy"]/section/div[2]/div[1]/div[2]/div[4]/table')
    # ss_dict = add_rows(inc, ss_dict)
    #
    # # balance sheet
    # bal = tree.xpath('//*[@id="Col1-3-KeyStatistics-Proxy"]/section/div[2]/div[1]/div[2]/div[5]/table')
    # ss_dict = add_rows(bal, ss_dict)
    #
    # # cash flow statement
    # cfs = tree.xpath('//*[@id="Col1-3-KeyStatistics-Proxy"]/section/div[2]/div[1]/div[2]/div[6]/table')
    # ss_dict = add_rows(cfs, ss_dict)
    #
    # # stock price history
    # sph = tree.xpath('//*[@id="Col1-3-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/table')
    # ss_dict = add_rows(sph, ss_dict)

    # one more table to add...meh


def scrape_all_tickers(tickers):
    full_df = None
    for t in tickers:
        print(t)
        df = scrape_stats(t)
        if full_df is None:
            full_df = df
        else:
            full_df = full_df.append(df)

    return full_df


def scrape_tickers_threads(tickers):
    """
    need to write to a mongodb before implementing this, for concurrent writes
    """
    tik = np.array(tickers)
    chunk_size = tik.shape[0] // 20
    tiks = list(np.split(tik, 20))
    if chunk_size != tik.shape[0] / 20:
        tiks.append(tik[chunk_size * 20:])

    for ti in tiks
        t = threading.Thread(target=scrape_all_tickers_mongo, args=(ti,))
        t.start()
        threads.append(t)
        for th in threads:
            th.join()
