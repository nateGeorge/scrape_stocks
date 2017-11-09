"""
scrapes data from here:
http://regsho.finra.org/regsho-Index.html


"""

# core
import os
import glob
import time

# installed
import requests as req
from bs4 import BeautifulSoup as bs
import urllib
import pandas as pd
from tqdm import tqdm

# custom
import scrape_stockdata as ss
from utils import get_home_dir

HOME_DIR = get_home_dir(repo_name='scrape_stocks')
FOLDERS = ['ADF', 'NASDAQ', 'NYSE', 'ORF']


def dl_and_get_df(ul, org):
    """
    :param ul: html of ul with links
    :param org: the organization, one of ['ADF', 'NASDAQ', 'NYSE', 'ORF']
    """
    if not os.path.exists('data'):
        os.mkdir('data')

    if not os.path.exists('data/' + org):
        os.mkdir('data/' + org)

    dfs = []
    for l in ul.find_all('li'):
        link = l.find('a').attrs['href']
        filename = link.split('/')[-1]
        urllib.request.urlretrieve(link, 'data/' + org + '/' + filename)
        df = pd.read_csv('data/' + org + '/' + filename, sep='|')
        nona = df.dropna()
        if df.shape != nona.shape and df.shape[0] == 1:
            print('empty file!')
            continue

        dfs.append(nona)

    if len(dfs) == 0:
        return None

    full_df = pd.concat(dfs)

    return full_df.dropna()


def get_lists(url, verbose=False):
    res = req.get(url, timeout=20)
    soup = bs(res.content, 'lxml')
    lists = soup.find_all('ul')
    uls = []
    for l in lists:
        ls = l.find_all('li')
        if len(ls) < 10:
            if verbose:
                print('list length is', len(ls))
                print('skipping')
        else:
            uls.append(l)

    return uls


def get_idx(verbose=False):
    url = 'http://regsho.finra.org/regsho-Index.html'
    res = req.get(url, timeout=20)
    soup = bs(res.content, 'lxml')
    lists = soup.find_all('ul')
    uls = []
    for l in lists:
        ls = l.find_all('li')
        if len(ls) < 10:
            if verbose:
                print('list length is', len(ls))
                print('skipping')
        else:
            uls.append(l)

    if len(uls) == 0:
        # then we skipped all the lists because it's early in the month
        uls = lists[1:5]

    tables = soup.find_all('table')
    month_links = [t.attrs['href'] for t in tables[1].find_all('a')]

    return uls, month_links


def get_current_files(fullpath=False):
    files = []
    for f in FOLDERS:
        filenames = HOME_DIR + 'data/' + f + '/*.txt'
        if fullpath:
            files.extend(glob.glob(filenames))
        else:
            files.extend([f.split('/')[-1] for f in glob.glob(filenames)])

    return files


def get_filenames(links):
    fns = []
    for l in links:
        fns.append(l.split('/')[-1])

    return fns


def get_org(filename):
    lookup_dict = {'FORF': 'ORF', 'FNYX': 'NYSE', 'FNRA': 'ADF', 'FNSQ': 'NASDAQ'}
    return lookup_dict[filename[:4]]


def update_data(check_all_months=True, verbose=False):
    """
    Right now kind of a brute-force approach to check all months at once.
    A better way would be one at a time but meh.  Not that expensive to do.
    """
    cur_files = set(get_current_files())
    uls, month_links = get_idx(verbose=verbose)

    links = []
    for u, o in zip(uls, ['ADF', 'NASDAQ', 'NYSE', 'ORF']):
        for l in u.find_all('li'):
            links.append(l.find('a').attrs['href'])

    if check_all_months:
        for m in month_links:
            uls = get_lists(m, verbose=verbose)
            for u, o in zip(uls, ['ADF', 'NASDAQ', 'NYSE', 'ORF']):
                for l in u.find_all('li'):
                    links.append(l.find('a').attrs['href'])

    filenames = get_filenames(links)
    fn_dict = {f: l for f, l in zip(filenames, links)}
    filenames = set(filenames)
    missing_files = filenames.difference(cur_files)
    print('missing', len(missing_files), 'files')

    for f in missing_files:
        link = fn_dict[f]
        org = get_org(f)
        urllib.request.urlretrieve(link, 'data/' + org + '/' + f)


def load_all_data(verbose=False):
    cur_files = get_current_files(fullpath=True)
    full_df = None
    dfs = []
    for f in tqdm(cur_files):
        df = pd.read_csv(f, sep='|')
        nona = df.dropna()
        if df.shape != nona.shape and df.shape[0] == 1:
            if verbose:
                print('empty file!')

            continue

        dfs.append(nona)

    return pd.concat(dfs)


def process_df(full_df):
    # if you want to separate by market...
    # grp = full_df.groupby(['Symbol', 'Date', 'Market']).sum()
    grp = full_df.groupby(['Symbol', 'Date']).sum()
    # get individual stocks
    navi = grp.loc['NAVI', :]
    navi.index = pd.to_datetime(navi.index, format='%Y%m%d')
    navi[(navi.index >= '2017-10-01') & (navi.index <= '2017-10-13')].sum()
    navi[(navi.index >= '2017-10-01') & (navi.index <= '2017-10-13')].mean()
    import matplotlib.pyplot as plt
    plt.plot(navi.index, navi.ShortVolume)  # need to get working with plot_date
    plt.plot(navi.index, navi.TotalVolume)
    plt.show()
    # combine with historical data


def daily_scrape_data():
    """
    checks if the market is open today or if we haven't scraped yet today,
    every hour.  If we haven't, scrapes data into the mongodb.

    basically the same as the function in scrape_stockdata.py
    """
    last_scrape = None
    while True:
        today_utc = pd.to_datetime('now')
        # today = datetime.datetime.now(pytz.timezone('America/New_York')).date()
        if last_scrape != today_utc.date():
            open_days = ss.check_market_status()
            if open_days is not None:
                if today_utc.hour > open_days.loc[today_utc.date()]['market_close'].hour:
                    latest_scrape = today_utc.date()
                    print('scraping...')
                    update_data(check_all_months=True)
                else:
                    # need to make it wait number of hours until close
                    print('waiting for market to close, waiting 1 hour...')
                    time.sleep(3600)
            else:
                # need to wait till market will be open then closed next
                print('market closed today, waiting 1 hour...')
                time.sleep(3600)  # wait 1 hour
        else:
            # need to make this more intelligent so it waits until the next day
            print('already scraped today, waiting 1 hour to check again...')
            time.sleep(3600)


if __name__ == "__main__":
    update_data(check_all_months=True)
    # uls, month_links = get_idx()
    # dfs = {}
    # for u, o in zip(uls, ['ADF', 'NASDAQ', 'NYSE', 'ORF']):
    #     dfs[o] = dl_and_get_df(u, o)
    #
    #
    # for m in month_links:
    #     print('getting data for month', m.split('-')[-1].split('.')[0])
    #     uls = get_lists(m)
    #     for u, o in zip(uls, ['ADF', 'NASDAQ', 'NYSE', 'ORF']):
    #         if dfs[o] is None:
    #             dfs[o] = dl_and_get_df(u, o)
    #         else:
    #             dfs[o] = dfs[o].append(dl_and_get_df(u, o))
    #
    # for d in dfs:
    #     pass
