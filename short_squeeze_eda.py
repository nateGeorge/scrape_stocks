# core
import os
import glob
import calendar

# installed
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

# custom
from utils import get_home_dir

HOME_DIR = get_home_dir(repo_name='scrape_stocks')

def load_parse_excel(f, dates_df, rev_cal_dict, verbose=False):
    if verbose:
        print(f)

    df = pd.read_excel(f)
    # fixes truecar ticker error; is listed as '1' in the data
    tc_idx = df[df['ShortSqueeze.com™ Short Interest Data'] == 'Truecar Incorporated'].index[0]
    df.at[tc_idx, 'Symbol'] = 'TRUE'
    # df.set_value(tc_idx, 'Symbol', 'TRUE')  # old way of doing it
    # cuts off crap at the end -- old way of doing it was too verbose, so commentetd out
    # end_idxs = df.index[df.iloc[:, 0].str.contains('ShortSqueeze.com: Master Spreadsheet', case=False).fillna(False) | df.iloc[:, 0].str.contains('ShortSqueeze.comï¿½: Master Spreadsheetï¿½ ', case=False).fillna(False)]
    end_idxs = df.index[df.iloc[:, 0].str.contains('Master Spreadsheet', case=False).fillna(False)]
    if len(end_idxs) > 1:
        print('WARNING: matched more than 1 end index at end of spreadsheet')
    elif len(end_idxs) < 1:
        print('WARNING: no end index found for:', f)

    # drop the end junk, and the fully missing rows (usually 2 at the end)
    df = df.iloc[:end_idxs[0]]
    df.drop(df.index[df.isnull().all(1)], inplace=True)
    df['Date'] = parse_bimo_dates(filename, dates_df, rev_cal_dict)
    if df['Symbol'].str.contains('AA-').sum() != 0 and verbose:
        print('contains AA-:', f)

    return df


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


def load_all_short_squeeze_data(load_cached=True, verbose=False, debug=False):
    """
    loads all historical data
    :param load_cached: boolean, if true, will load an existing h5 file
    """
    filename = HOME_DIR + 'short_squeeze_data.h5'
    if os.path.exists(filename):
        cached_df = pd.read_hdf(filename)
    if load_cached:
        return cached_df

    cal_dict = {v: k for k, v in enumerate(calendar.month_name)}
    del cal_dict['']
    rev_cal_dict = {v: k for k, v in cal_dict.items()}

    dates_df = pd.read_excel(HOME_DIR + 'short_squeeze_release_dates.xlsx', None)

    # check if any files are newer than the latest date
    latest_date = cached_df['Date'].max()
    bimonthly_files = glob.glob(HOME_DIR + 'data/short_squeeze.com/*.xlsx')
    bimo_dates = [parse_bimo_dates(f, dates_df, rev_cal_dict) for f in bimonthly_files]

    # get latest date from daily scrapes
    daily_files = glob.glob(HOME_DIR + 'data/short_squeeze_daily/*.csv')
    daily_dates = [pd.to_datetime(f.split('/')[-1].split('.')[0]) for f in daily_files]

    latest_file_date = max(bimo_dates + daily_dates)
    latest_cache_date = cached_df['Date'].max()
    if latest_cache_date == latest_file_date:
        return cached_df


    dfs = []

    dfs = []
    if debug:
        for f in bimonhtly_files:
            df = load_parse_excel(f, dates_df, rev_cal_dict, verbose)
            dfs.append(df)
    else:
        jobs = []
        with ProcessPoolExecutor(max_workers=None) as executor:
            for f in bimonthly_files:
                r = executor.submit(load_parse_excel,
                                    f,
                                    dates_df,
                                    rev_cal_dict,
                                    verbose)
                jobs.append((f, r))

        for f, r in jobs:
            print(r)
            if r.result() is not None:
                dfs.append(r.result())

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


def get_short_interest_data(full_df=None, load_cached=False, debug=False):
    if full_df is None:
        full_df = load_all_short_squeeze_data(load_cached=load_cached, debug=debug)

    cols = ['Symbol',
            'Date',
            'Total Short Interest',
            'Days to Cover',
            'Short % of Float',
            '% Insider Ownership',
            '% Institutional Ownership',
            'Shares: Float',
            'Short Squeeze Ranking™']

    return full_df[cols].rename(columns={'Short Squeeze Ranking™': 'Short Squeeze Ranking'})


def get_stocks(ignore_plus_minus=True, load_cached=False):
    """
    returns stocks with data from shortsqueeze.com
    """
    full_df = load_all_short_squeeze_data(load_cached=load_cached)
    stks = sorted(full_df['Symbol'].unique())
    if ignore_plus_minus:
        stks = [s for s in stks if s[-1] not in ['+', '-']]

    return stks


def get_daily_files():
    """
    gets list of daily files and return latest date
    """
    files = glob.glob(HOME_DIR + 'data/short_squeeze_daily/*.csv')
