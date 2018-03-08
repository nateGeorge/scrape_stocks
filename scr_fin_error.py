scraping...
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
<ipython-input-4-2c9937c17e38> in <module>()
----> 1 daily_scrape_data()

~/github/scrape_stocks/scrape_finra_shorts.py in daily_scrape_data()
    223                     last_scrape = today_utc.date()
    224                     print('scraping...')
--> 225                     update_data(check_all_months=True)
    226                 else:
    227                     # need to make it wait number of hours until close

~/github/scrape_stocks/scrape_finra_shorts.py in update_data(check_all_months, verbose)
    132     """
    133     cur_files = set(get_current_files())
--> 134     uls, month_links = get_idx(verbose=verbose)
    135
    136     links = []

~/github/scrape_stocks/scrape_finra_shorts.py in get_idx(verbose)
     96
     97     tables = soup.find_all('table')
---> 98     month_links = [t.attrs['href'] for t in tables[1].find_all('a')]
     99
    100     return uls, month_links

IndexError: list index out of range
