ZYME
ticker not found
ZYNE
ERROR:root:Internal Python error in the inspect module.
Below is the traceback from this internal error.

concurrent.futures.process._RemoteTraceback:
"""
Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 601, in urlopen
    chunked=chunked)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 387, in _make_request
    six.raise_from(e, None)
  File "<string>", line 2, in raise_from
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 383, in _make_request
    httplib_response = conn.getresponse()
  File "/usr/lib/python3.5/http/client.py", line 1197, in getresponse
    response.begin()
  File "/usr/lib/python3.5/http/client.py", line 297, in begin
    version, status, reason = self._read_status()
  File "/usr/lib/python3.5/http/client.py", line 266, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/requests/adapters.py", line 440, in send
    timeout=timeout
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 639, in urlopen
    _stacktrace=sys.exc_info()[2])
  File "/usr/local/lib/python3.5/dist-packages/urllib3/util/retry.py", line 357, in increment
    raise six.reraise(type(error), error, _stacktrace)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/packages/six.py", line 685, in reraise
    raise value.with_traceback(tb)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 601, in urlopen
    chunked=chunked)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 387, in _make_request
    six.raise_from(e, None)
  File "<string>", line 2, in raise_from
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 383, in _make_request
    httplib_response = conn.getresponse()
  File "/usr/lib/python3.5/http/client.py", line 1197, in getresponse
    response.begin()
  File "/usr/lib/python3.5/http/client.py", line 297, in begin
    version, status, reason = self._read_status()
  File "/usr/lib/python3.5/http/client.py", line 266, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
urllib3.exceptions.ProtocolError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection
 without response',))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):                                                              [168/1972]
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
  File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 618, in send
    r = adapter.send(request, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/requests/adapters.py", line 490, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connect
ion without response',))
"""

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py", line 2910, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-2-2c9937c17e38>", line 1, in <module>
    daily_scrape_data()
  File "/home/nate/github/scrape_stocks/scrape_stockdata.py", line 641, in daily_scrape_data
    scrape_all_tickers_mongo_parallel()
  File "/home/nate/github/scrape_stocks/scrape_stockdata.py", line 551, in scrape_all_tickers_mongo_parall
el
    elif r.result() is not None:
  File "/usr/lib/python3.5/concurrent/futures/_base.py", line 398, in result
    return self.__get_result()
  File "/usr/lib/python3.5/concurrent/futures/_base.py", line 357, in __get_result
    raise self._exception
requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connect
ion without response',))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py", line 1828, in showtraceb
ack
    stb = value._render_traceback_()
AttributeError: 'ConnectionError' object has no attribute '_render_traceback_'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):                                                              [120/1972]
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py", line 1090, in get_records
    return _fixed_getinnerframes(etb, number_of_lines_of_context, tb_offset)
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py", line 311, in wrapped
    return f(*args, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py", line 345, in _fixed_getinnerframe
s
    records = fix_frame_records_filenames(inspect.getinnerframes(etb, context))
  File "/usr/lib/python3.5/inspect.py", line 1453, in getinnerframes
    frameinfo = (tb.tb_frame,) + getframeinfo(tb, context)
  File "/usr/lib/python3.5/inspect.py", line 1410, in getframeinfo
    filename = getsourcefile(frame) or getfile(frame)
  File "/usr/lib/python3.5/inspect.py", line 672, in getsourcefile
    if getattr(getmodule(object, filename), '__loader__', None) is not None:
  File "/usr/lib/python3.5/inspect.py", line 718, in getmodule
    os.path.realpath(f)] = module.__name__
AttributeError: module has no attribute '__name__'
---------------------------------------------------------------------------
_RemoteTraceback                          Traceback (most recent call last)
_RemoteTraceback:
"""
Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 601, in urlopen
    chunked=chunked)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 387, in _make_request
    six.raise_from(e, None)
  File "<string>", line 2, in raise_from
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 383, in _make_request
    httplib_response = conn.getresponse()
  File "/usr/lib/python3.5/http/client.py", line 1197, in getresponse
    response.begin()
  File "/usr/lib/python3.5/http/client.py", line 297, in begin
    version, status, reason = self._read_status()
  File "/usr/lib/python3.5/http/client.py", line 266, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/requests/adapters.py", line 440, in send
    timeout=timeout
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 639, in urlopen
    _stacktrace=sys.exc_info()[2])
  File "/usr/local/lib/python3.5/dist-packages/urllib3/util/retry.py", line 357, in increment
    raise six.reraise(type(error), error, _stacktrace)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/packages/six.py", line 685, in reraise
    raise value.with_traceback(tb)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 601, in urlopen
    chunked=chunked)
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 387, in _make_request
    six.raise_from(e, None)
  File "<string>", line 2, in raise_from
  File "/usr/local/lib/python3.5/dist-packages/urllib3/connectionpool.py", line 383, in _make_request
    httplib_response = conn.getresponse()
  File "/usr/lib/python3.5/http/client.py", line 1197, in getresponse
    response.begin()
    File "/usr/lib/python3.5/http/client.py", line 297, in begin
  version, status, reason = self._read_status()
File "/usr/lib/python3.5/http/client.py", line 266, in _read_status
  raise RemoteDisconnected("Remote end closed connection without"
urllib3.exceptions.ProtocolError: ('Connection aborted.', RemoteDisconnected('Remote end closed connectio$
without response',))

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
File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 618, in send
  r = adapter.send(request, **kwargs)
File "/usr/local/lib/python3.5/dist-packages/requests/adapters.py", line 490, in send
  raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connect
ion without response',))
"""

The above exception was the direct cause of the following exception:

ConnectionError                           Traceback (most recent call last)
/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py in run_code(self, code_obj, result
)
 2909                 #rprint('Running code', repr(code_obj)) # dbg
-> 2910                 exec(code_obj, self.user_global_ns, self.user_ns)
 2911             finally:

<ipython-input-2-2c9937c17e38> in <module>()
----> 1 daily_scrape_data()

~/github/scrape_stocks/scrape_stockdata.py in daily_scrape_data()
  640                     print('scraping...')
--> 641                     scrape_all_tickers_mongo_parallel()
  642                 else:

~/github/scrape_stocks/scrape_stockdata.py in scrape_all_tickers_mongo_parallel(tickers)
  550             print('ticker:', t, 'job result is None')
--> 551         elif r.result() is not None:
  552             print('ticker:', t, 'result:', r.result())

/usr/lib/python3.5/concurrent/futures/_base.py in result(self, timeout)
  397             elif self._state == FINISHED:
--> 398                 return self.__get_result()
  399

  /usr/lib/python3.5/concurrent/futures/_base.py in __get_result(self)
      356         if self._exception:
  --> 357             raise self._exception
      358         else:

  ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without respons$
  ',))

  During handling of the above exception, another exception occurred:

  AttributeError                            Traceback (most recent call last)
  /usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py in showtraceback(self, exc_tuple,
  filename, tb_offset, exception_only, running_compiled_code)
     1827                         # in the engines. This should return a list of strings.
  -> 1828                         stb = value._render_traceback_()
     1829                     except Exception:

  AttributeError: 'ConnectionError' object has no attribute '_render_traceback_'

  During handling of the above exception, another exception occurred:

  TypeError                                 Traceback (most recent call last)
  /usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py in run_code(self, code_obj, resul$
  )
     2925             if result is not None:
     2926                 result.error_in_exec = sys.exc_info()[1]
  -> 2927             self.showtraceback(running_compiled_code=True)
     2928         else:
     2929             outflag = False

  /usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py in showtraceback(self, exc_tuple,
  filename, tb_offset, exception_only, running_compiled_code)
     1829                     except Exception:
     1830                         stb = self.InteractiveTB.structured_traceback(etype,
  -> 1831                                             value, tb, tb_offset=tb_offset)
     1832
     1833                     self._showtraceback(etype, value, stb)

  /usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py in structured_traceback(self, etype, value,
   tb, tb_offset, number_of_lines_of_context)
     1369         self.tb = tb
     1370         return FormattedTB.structured_traceback(
  -> 1371             self, etype, value, tb, tb_offset, number_of_lines_of_context)
     1372
     1373

  /usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py in structured_traceback(self, etype, value,
   tb, tb_offset, number_of_lines_of_context)
     1277             # Verbose modes need a full traceback
     1278             return VerboseTB.structured_traceback(
  -> 1279                 self, etype, value, tb, tb_offset, number_of_lines_of_context
     1280             )
     1281         else:

     /usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py in structured_traceback(self, etype, evalue
     , etb, tb_offset, number_of_lines_of_context)
        1138             exception = self.get_parts_of_chained_exception(evalue)
        1139             if exception:
     -> 1140                 formatted_exceptions += self.prepare_chained_exception_message(evalue.__cause__)
        1141                 etype, evalue, etb = exception
        1142             else:

     TypeError: Can't convert 'list' object to str implicitly
