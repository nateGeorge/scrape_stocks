ZYNE
---------------------------------------------------------------------------
_RemoteTraceback                          Traceback (most recent call last)
_RemoteTraceback:
"""
Traceback (most recent call last):
  File "/usr/lib/python3.5/concurrent/futures/process.py", line 175, in _process_worker
    r = call_item.fn(*call_item.args, **call_item.kwargs)
  File "/home/nate/github/scrape_stocks/scrape_stockdata.py", line 595, in scrape_a_ticker_mongo
    for k in res.json()['quoteSummary']['result'][0].keys():
TypeError: 'NoneType' object is not subscriptable
"""

The above exception was the direct cause of the following exception:

TypeError                                 Traceback (most recent call last)
<ipython-input-4-d000891ab129> in <module>()
----> 1 scrape_all_tickers_mongo_parallel()

~/github/scrape_stocks/scrape_stockdata.py in scrape_all_tickers_mongo_parallel(tickers)
    554         if r is None:
    555             print('ticker:', t, 'job result is None')
--> 556         elif r is not None and r.result() is not None:
    557             print('ticker:', t, 'result:', r.result())
    558     # old way of doing it, and wasn't working great

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
