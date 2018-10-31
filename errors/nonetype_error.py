ZYME
ZYNE
---------------------------------------------------------------------------
_RemoteTraceback                          Traceback (most recent call last)
_RemoteTraceback:
"""
Traceback (most recent call last):
  File "/usr/lib/python3.5/concurrent/futures/process.py", line 175, in _process_worker
    r = call_item.fn(*call_item.args, **call_item.kwargs)
  File "/home/nate/github/scrape_stocks/scrape_stockdata.py", line 590, in scrape_a_ticker_mongo
    for k in res.json()['quoteSummary']['result'][0].keys():
TypeError: 'NoneType' object is not subscriptable
"""

The above exception was the direct cause of the following exception:

TypeError                                 Traceback (most recent call last)
<ipython-input-7-2c9937c17e38> in <module>()
----> 1 daily_scrape_data()

~/github/scrape_stocks/scrape_stockdata.py in daily_scrape_data()
    639                     last_scrape = today_utc.date()
    640                     print('scraping...')
--> 641                     scrape_all_tickers_mongo_parallel()
    642                 else:
    643                     # need to make it wait number of hours until close

~/github/scrape_stocks/scrape_stockdata.py in scrape_all_tickers_mongo_parallel(tickers)
    549         if r is None:
    550             print('ticker:', t, 'job result is None')
--> 551         elif r.result() is not None:
    552             print('ticker:', t, 'result:', r.result())
    553     # old way of doing it, and wasn't working great

/usr/lib/python3.5/concurrent/futures/_base.py in result(self, timeout)
    396                 raise CancelledError()
    397             elif self._state == FINISHED:
--> 398                 return self.__get_result()
    399
    400             self._condition.wait(timeout)

/usr/lib/python3.5/concurrent/futures/_base.py in __get_result(self)
    355     def __get_result(self):
    356         if self._exception:
--> 357             raise self._exception
    358         else:
    359             return self._result

TypeError: 'NoneType' object is not subscriptable
