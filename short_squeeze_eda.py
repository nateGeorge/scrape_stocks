# core
import os
import glob
import calendar

# installed
import pandas as pd
from tqdm import tqdm

# custom
from utils import get_home_dir

HOME_DIR = get_home_dir(repo_name='scrape_stocks')

def load_all_short_squeeze_data():
    filename = 'short_squeeze_data.h5'
    if os.path.exists(filename):
        return pd.read_hdf(filename)

    cal_dict = {v: k for k, v in enumerate(calendar.month_name)}
    del cal_dict['']
    rev_cal_dict = {v: k for k, v in cal_dict.items()}

    dates_df = pd.read_excel('short_squeeze_release_dates.xlsx', None)

    dfs = []
    files = glob.glob(HOME_DIR + 'data/short_squeeze.com/*.xlsx')
    for f in tqdm(files):
        df = pd.read_excel(f)
        date = f.split('/')[-1][9:16]
        year = date[:4]
        month_num = int(date[4:6])
        month = rev_cal_dict[month_num]
        ab = date[-1].upper()
        t_df = dates_df[year]
        date = '-'.join([year,
                        str(month_num).zfill(2),
                        str(t_df[t_df[int(year)] == (month + ' ' + ab)]['NASDAQ®'].values[0]).zfill(2)])
        date = pd.to_datetime(date, format='%Y-%m-%d')
        df['date'] = date
        dfs.append(df)

    full_df = pd.concat(dfs)
    drop_cols = ['Record Date',
                'Price',
                'Exchange',
                'Market Cap',
                'ShortSqueeze.com™ Short Interest Data',
                'Sector',
                'Industry',
                '(abs)',
                '(abs).1',
                '(abs).2',]
    full_df.drop(drop_cols, inplace=True, axis=1)
    full_df.to_hdf(filename, key='data', complib='blosc', complevel=9)
    return full_df


def get_short_interest_cols(full_df=None):
    if full_df is None:
        full_df = load_all_short_squeeze_data()
    cols = ['Symbol',
            'date',
            'Total Short Interest',
            'Days to Cover',
            'Short % of Float',
            '% Insider Ownership',
            '% Institutional Ownership',
            'Shares: Float',
            'Short Squeeze Ranking™']

    return full_df[cols]
