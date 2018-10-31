ZYME
ZYNE
---------------------------------------------------------------------------
_RemoteTraceback                          Traceback (most recent call last)
_RemoteTraceback:
"""
Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/urllib3/contrib/pyopenssl.py", line 280, in recv_into
    return self.connection.recv_into(*args, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/OpenSSL/SSL.py", line 1547, in recv_into
    self._raise_ssl_error(self._ssl, result)
  File "/usr/local/lib/python3.5/dist-packages/OpenSSL/SSL.py", line 1353, in _raise_ssl_error
    raise WantReadError()
OpenSSL.SSL.WantReadError

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/urllib3/response.py", line 302, in _error_catcher
    yield
  File "/usr/local/lib/python3.5/dist-packages/urllib3/response.py", line 384, in read
    data = self._fp.read(amt)
  File "/usr/lib/python3.5/http/client.py", line 448, in read
    n = self.readinto(b)
  File "/usr/lib/python3.5/http/client.py", line 488, in readinto
    n = self.fp.readinto(b)
  File "/usr/lib/python3.5/socket.py", line 575, in readinto
    return self._sock.recv_into(b)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/contrib/pyopenssl.py", line 294, in recv_into
    raise timeout('The read operation timed out')
socket.timeout: The read operation timed out

During handling of the above exception, another exception occurred:


Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/requests/models.py", line 745, in generate
    for chunk in self.raw.stream(chunk_size, decode_content=True):
  File "/usr/local/lib/python3.5/dist-packages/urllib3/response.py", line 436, in stream
    data = self.read(amt=amt, decode_content=decode_content)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/response.py", line 401, in read
    raise IncompleteRead(self._fp_bytes_read, self.length_remaining)
  File "/usr/lib/python3.5/contextlib.py", line 77, in __exit__
    self.gen.throw(type, value, traceback)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/response.py", line 307, in _error_catcher
    raise ReadTimeoutError(self._pool, None, 'Read timed out.')
urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='query2.finance.yahoo.com', port=443): Read
timed out.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.5/concurrent/futures/process.py", line 175, in _process_worker
    r = call_item.fn(*call_item.args, **call_item.kwargs)
  File "/home/nate/github/scrape_stocks/scrape_stockdata.py", line 571, in scrape_a_ticker_mongo
    res = req.get(url, timeout=10)
  File "/usr/local/lib/python3.5/dist-packages/requests/api.py", line 72, in get
    return request('get', url, params=params, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/requests/api.py", line 58, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 508, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 658, in send
    r.content
  File "/usr/local/lib/python3.5/dist-packages/requests/models.py", line 823, in content
    self._content = bytes().join(self.iter_content(CONTENT_CHUNK_SIZE)) or bytes()
  File "/usr/local/lib/python3.5/dist-packages/requests/models.py", line 752, in generate
    raise ConnectionError(e)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='query2.finance.yahoo.com', port=443): Read
timed out.
"""

The above exception was the direct cause of the following exception:

ConnectionError                           Traceback (most recent call last)
<ipython-input-5-2c9937c17e38> in <module>()
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

ConnectionError: None: None
