"""
scrapes data from here:
http://regsho.finra.org/regsho-Index.html


"""

# core
import os

# installed
import requests as req
from bs4 import BeautifulSoup as bs
import urllib
import pandas as pd


def dl_and_get_df(ul, org):
    """
    :param ul: html of ul with links
    :param org: the organization, one of ['ADF', 'NASDAQ', 'NYSE', 'ORF']
    """
    if not os.path.exists('data'):
        os.mkdir('data')

    if not os.path.exists('data/' + org):
        os.mkdir('data/' + org)

    full_df = None
    for l in ul.find_all('li'):
        link = l.find('a').attrs['href']
        filename = link.split('/')[-1]
        urllib.request.urlretrieve(link, 'data/' + org + '/' + filename)
        df = pd.read_csv('data/' + org + '/' + filename, sep='|')
        nona = df.dropna()
        if df.shape != nona.shape and df.shape[0] == 1:
            print('empty file!')
            continue

        if full_df is None:
            full_df = df
        else:
            full_df = full_df.append(df)

    if full_df is None:
        return None

    return full_df.dropna()


def get_lists(url):
    res = req.get(url, timeout=20)
    soup = bs(res.content, 'lxml')
    lists = soup.find_all('ul')
    uls = []
    for l in lists:
        ls = l.find_all('li')
        if len(ls) < 10:
            print('list length is', len(ls))
            print('skipping')
        else:
            uls.append(l)

    return uls


def get_idx():
    url = 'http://regsho.finra.org/regsho-Index.html'
    res = req.get(url, timeout=20)
    soup = bs(res.content, 'lxml')
    lists = soup.find_all('ul')
    uls = []
    for l in lists:
        ls = l.find_all('li')
        if len(ls) < 10:
            print('list length is', len(ls))
            print('skipping')
        else:
            uls.append(l)

    tables = soup.find_all('table')
    month_links = [t.attrs['href'] for t in tables[1].find_all('a')]

    return uls, month_links


def load_current_files():
    


def update_data():



if __name__ == "__main__":
    uls, month_links = get_idx()
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
