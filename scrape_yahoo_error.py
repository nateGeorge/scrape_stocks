ticker not found
---------------------------------------------------------------------------
_RemoteTraceback                          Traceback (most recent call last)
_RemoteTraceback:
"""
Traceback (most recent call last):
  File "/home/nate/anaconda3/lib/python3.6/concurrent/futures/process.py", line 175, in _process_worker
    r = call_item.fn(*call_item.args, **call_item.kwargs)
  File "/media/nate/nates/github/scrape_stocks/scrape_stockdata.py", line 591, in scrape_a_ticker_mongo
    if res.json()['quoteSummary']['result'] is None and res.json()['quoteSummary']['error']['code'] == 'Not Found':
  File "/home/nate/anaconda3/lib/python3.6/site-packages/requests/models.py", line 897, in json
    return complexjson.loads(self.text, **kwargs)
  File "/home/nate/anaconda3/lib/python3.6/json/__init__.py", line 354, in loads
    return _default_decoder.decode(s)
  File "/home/nate/anaconda3/lib/python3.6/json/decoder.py", line 339, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/home/nate/anaconda3/lib/python3.6/json/decoder.py", line 357, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
"""

The above exception was the direct cause of the following exception:

JSONDecodeError                           Traceback (most recent call last)
<ipython-input-1-2c9937c17e38> in <module>
----> 1 daily_scrape_data()

/media/nate/nates/github/scrape_stocks/scrape_stockdata.py in daily_scrape_data()
    661                     last_scrape = today_ny.date()
    662                     print('scraping...')
--> 663                     scrape_all_tickers_mongo_parallel()
    664                     write_backup_file()
    665                 else:

/media/nate/nates/github/scrape_stocks/scrape_stockdata.py in scrape_all_tickers_mongo_parallel(tickers)
    556         if r is None:
    557             print('ticker:', t, 'job result is None')
--> 558         elif r is not None and r.result() is not None:
    559             print('ticker:', t, 'result:', r.result())
    560     # old way of doing it, and wasn't working great

~/anaconda3/lib/python3.6/concurrent/futures/_base.py in result(self, timeout)
    423                 raise CancelledError()
    424             elif self._state == FINISHED:
--> 425                 return self.__get_result()
    426
    427             self._condition.wait(timeout)

~/anaconda3/lib/python3.6/concurrent/futures/_base.py in __get_result(self)
    382     def __get_result(self):
    383         if self._exception:
--> 384             raise self._exception
    385         else:
    386             return self._result

JSONDecodeError: Expecting value: line 1 column 1 (char 0)
