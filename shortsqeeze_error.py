more than 1 day out of date, downloading...
nothing to scrape right now
downloading http://shortsqueeze.com/shortint.201801a-09kug6f5esd678uhi.xlsx
/home/nate/Downloads/shortint.201801a-09kug6f5esd678uhi.xlsx
sleeping 1h...
more than 1 day out of date, downloading...
nothing to scrape right now
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
~/github/scrape_stocks/scrape_shortsqueeze.py in <module>()
    319     driver = log_in(driver)
    320     time.sleep(3)  # wait for login to complete...could also use some element detection
--> 321     daily_updater(driver)

~/github/scrape_stocks/scrape_shortsqueeze.py in daily_updater(driver)
    274             print('more than 1 day out of date, downloading...')
    275             download_daily_data(driver)
--> 276             check_for_new_excel(driver)
    277         elif (latest_close_date.date() - latest_scrape) == pd.Timedelta('1D'):
    278             if today_utc.hour > latest_close_date.hour:

~/github/scrape_stocks/scrape_shortsqueeze.py in check_for_new_excel(driver)
     97     bimonthly_files = glob.glob(HOME_DIR + 'data/short_squeeze.com/*.xlsx')
     98     bimonthly_filenames = set([f.split('/')[-1] for f in bimonthly_files])
---> 99     bimo_dates = [parse_bimo_dates(f, dates_df, rev_cal_dict) for f in bimonthly_files]
    100     latest_date = max(bimo_dates).date()
    101     latest_year = latest_date.year

~/github/scrape_stocks/scrape_shortsqueeze.py in <listcomp>(.0)
     97     bimonthly_files = glob.glob(HOME_DIR + 'data/short_squeeze.com/*.xlsx')
     98     bimonthly_filenames = set([f.split('/')[-1] for f in bimonthly_files])
---> 99     bimo_dates = [parse_bimo_dates(f, dates_df, rev_cal_dict) for f in bimonthly_files]
    100     latest_date = max(bimo_dates).date()
    101     latest_year = latest_date.year

~/github/scrape_stocks/scrape_shortsqueeze.py in parse_bimo_dates(filename, dates_df, rev_cal_dict)
     74     month = rev_cal_dict[month_num]
     75     ab = date[-1].upper()
---> 76     t_df = dates_df[year]
     77     date = '-'.join([year,
     78                     str(month_num).zfill(2),

KeyError: '2018'
