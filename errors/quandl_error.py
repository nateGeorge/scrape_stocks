sleeping 1h...
db more than 1 day out of date, downloading...
ERROR:root:Internal Python error in the inspect module.
Below is the traceback from this internal error.

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/urllib3/contrib/pyopenssl.py", line 280, in recv_into
    return self.connection.recv_into(*args, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/OpenSSL/SSL.py", line 1547, in recv_into
    self._raise_ssl_error(self._ssl, result)
  File "/usr/local/lib/python3.5/dist-packages/OpenSSL/SSL.py", line 1370, in _raise_ssl_error
    raise SysCallError(errno, errorcode.get(errno))
OpenSSL.SSL.SysCallError: (104, 'ECONNRESET')

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
  File "/usr/local/lib/python3.5/dist-packages/urllib3/contrib/pyopenssl.py", line 285, in recv_into
    raise SocketError(str(e))
OSError: (104, 'ECONNRESET')

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
  File "/usr/local/lib/python3.5/dist-packages/urllib3/response.py", line 320, in _error_catcher
    raise ProtocolError('Connection broken: %r' % e, e)
urllib3.exceptions.ProtocolError: ('Connection broken: OSError("(104, \'ECONNRESET\')",)', OSError("(104,
'ECONNRESET')",))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py", line 2910, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-2-fc44acddff0e>", line 1, in <module>
    daily_download_entire_db()
  File "/home/nate/github/stock_prediction/code/dl_quandl_EOD.py", line 156, in daily_download_entire_db
    latest_db_date = download_entire_db(return_latest_date=True)
  File "/home/nate/github/stock_prediction/code/dl_quandl_EOD.py", line 93, in download_entire_db
    r = req.get(zip_file_url)
  File "/usr/local/lib/python3.5/dist-packages/requests/api.py", line 72, in get
return request('get', url, params=params, **kwargs)
File "/usr/local/lib/python3.5/dist-packages/requests/api.py", line 58, in request
return session.request(method=method, url=url, **kwargs)
File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 508, in request
resp = self.send(prep, **send_kwargs)
File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 640, in send
history = [resp for resp in gen] if allow_redirects else []
File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 640, in <listcomp>
history = [resp for resp in gen] if allow_redirects else []
File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 218, in resolve_redirects
**adapter_kwargs
File "/usr/local/lib/python3.5/dist-packages/requests/sessions.py", line 658, in send
r.content
File "/usr/local/lib/python3.5/dist-packages/requests/models.py", line 823, in content
self._content = bytes().join(self.iter_content(CONTENT_CHUNK_SIZE)) or bytes()
File "/usr/local/lib/python3.5/dist-packages/requests/models.py", line 748, in generate
raise ChunkedEncodingError(e)
requests.exceptions.ChunkedEncodingError: ('Connection broken: OSError("(104, \'ECONNRESET\')",)', OSError
("(104, 'ECONNRESET')",))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
File "/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py", line 1828, in showtraceb
ack
stb = value._render_traceback_()
AttributeError: 'ChunkedEncodingError' object has no attribute '_render_traceback_'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
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
SysCallError                              Traceback (most recent call last)
/usr/local/lib/python3.5/dist-packages/urllib3/contrib/pyopenssl.py in recv_into(self, *args, **kwargs)
    279         try:
--> 280             return self.connection.recv_into(*args, **kwargs)
    281         except OpenSSL.SSL.SysCallError as e:

/usr/local/lib/python3.5/dist-packages/OpenSSL/SSL.py in recv_into(self, buffer, nbytes, flags)
   1546             result = _lib.SSL_read(self._ssl, buf, nbytes)
-> 1547         self._raise_ssl_error(self._ssl, result)
   1548

/usr/local/lib/python3.5/dist-packages/OpenSSL/SSL.py in _raise_ssl_error(self, ssl, result)
   1369                     if errno != 0:
-> 1370                         raise SysCallError(errno, errorcode.get(errno))
   1371                 raise SysCallError(-1, "Unexpected EOF")

SysCallError: (104, 'ECONNRESET')

During handling of the above exception, another exception occurred:

OSError                                   Traceback (most recent call last)
/usr/local/lib/python3.5/dist-packages/urllib3/response.py in _error_catcher(self)
    301             try:
--> 302                 yield
    303

/usr/local/lib/python3.5/dist-packages/urllib3/response.py in read(self, amt, decode_content, cache_conte$
t)
    383                 cache_content = False
--> 384                 data = self._fp.read(amt)
    385                 if amt != 0 and not data:  # Platform-specific: Buggy versions of Python.

/usr/lib/python3.5/http/client.py in read(self, amt)
    447             b = bytearray(amt)
--> 448             n = self.readinto(b)
    449             return memoryview(b)[:n].tobytes()

/usr/lib/python3.5/http/client.py in readinto(self, b)
    487         # (for example, reading in 1k chunks)
--> 488         n = self.fp.readinto(b)
    489         if not n and b:

/usr/lib/python3.5/socket.py in readinto(self, b)
    574             try:
--> 575                 return self._sock.recv_into(b)
    576             except timeout:

/usr/local/lib/python3.5/dist-packages/urllib3/contrib/pyopenssl.py in recv_into(self, *args, **kwargs)
    284             else:
--> 285                 raise SocketError(str(e))
    286         except OpenSSL.SSL.ZeroReturnError as e:
OSError: (104, 'ECONNRESET')

During handling of the above exception, another exception occurred:

ProtocolError                             Traceback (most recent call last)
/usr/local/lib/python3.5/dist-packages/requests/models.py in generate()
    744                 try:
--> 745                     for chunk in self.raw.stream(chunk_size, decode_content=True):
    746                         yield chunk

/usr/local/lib/python3.5/dist-packages/urllib3/response.py in stream(self, amt, decode_content)
    435             while not is_fp_closed(self._fp):
--> 436                 data = self.read(amt=amt, decode_content=decode_content)
    437

/usr/local/lib/python3.5/dist-packages/urllib3/response.py in read(self, amt, decode_content, cache_conten
t)
    400                         # Content-Length are caught.
--> 401                         raise IncompleteRead(self._fp_bytes_read, self.length_remaining)
    402

/usr/lib/python3.5/contextlib.py in __exit__(self, type, value, traceback)
     76             try:
---> 77                 self.gen.throw(type, value, traceback)
     78                 raise RuntimeError("generator didn't stop after throw()")

/usr/local/lib/python3.5/dist-packages/urllib3/response.py in _error_catcher(self)
    319                 # This includes IncompleteRead.
--> 320                 raise ProtocolError('Connection broken: %r' % e, e)
    321

ProtocolError: ('Connection broken: OSError("(104, \'ECONNRESET\')",)', OSError("(104, 'ECONNRESET')",))

During handling of the above exception, another exception occurred:

ChunkedEncodingError                      Traceback (most recent call last)
/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py in run_code(self, code_obj, result
)
   2909                 #rprint('Running code', repr(code_obj)) # dbg
-> 2910                 exec(code_obj, self.user_global_ns, self.user_ns)
   2911             finally:

<ipython-input-2-fc44acddff0e> in <module>()
----> 1 daily_download_entire_db()

~/github/stock_prediction/code/dl_quandl_EOD.py in daily_download_entire_db(storage_path)
    155                     print('db more than 1 day out of date, downloading...')
--> 156                     latest_db_date = download_entire_db(return_latest_date=True)
    157             elif pd_today_ny.date() == latest_close_date.date():  # if the market is open and the
db isn't up to date with today...

~/github/stock_prediction/code/dl_quandl_EOD.py in download_entire_db(storage_path, remove_last, return_df
, return_latest_date)
     92     zip_file_url = 'https://www.quandl.com/api/v3/databases/EOD/data?api_key=' + Q_KEY
---> 93     r = req.get(zip_file_url)
     94     z = zipfile.ZipFile(io.BytesIO(r.content))

/usr/local/lib/python3.5/dist-packages/requests/api.py in get(url, params, **kwargs)
     71     kwargs.setdefault('allow_redirects', True)
---> 72     return request('get', url, params=params, **kwargs)
     73

/usr/local/lib/python3.5/dist-packages/requests/api.py in request(method, url, **kwargs)
     57     with sessions.Session() as session:
---> 58         return session.request(method=method, url=url, **kwargs)
     59

/usr/local/lib/python3.5/dist-packages/requests/sessions.py in request(self, method, url, params, data, he
aders, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
    507         send_kwargs.update(settings)
--> 508         resp = self.send(prep, **send_kwargs)
    509

/usr/local/lib/python3.5/dist-packages/requests/sessions.py in send(self, request, **kwargs)
    639         # Resolve redirects if allowed.
--> 640         history = [resp for resp in gen] if allow_redirects else []
    641

/usr/local/lib/python3.5/dist-packages/requests/sessions.py in <listcomp>(.0)
    639         # Resolve redirects if allowed.
--> 640         history = [resp for resp in gen] if allow_redirects else []
    641

/usr/local/lib/python3.5/dist-packages/requests/sessions.py in resolve_redirects(self, resp, req, stream,
timeout, verify, cert, proxies, yield_requests, **adapter_kwargs)
    217                     allow_redirects=False,
--> 218                     **adapter_kwargs
    219                 )

/usr/local/lib/python3.5/dist-packages/requests/sessions.py in send(self, request, **kwargs)
    657         if not stream:
--> 658             r.content
    659

/usr/local/lib/python3.5/dist-packages/requests/models.py in content(self)
    822             else:
--> 823                 self._content = bytes().join(self.iter_content(CONTENT_CHUNK_SIZE)) or bytes()
    824

/usr/local/lib/python3.5/dist-packages/requests/models.py in generate()
    747                 except ProtocolError as e:
--> 748                     raise ChunkedEncodingError(e)
    749                 except DecodeError as e:

ChunkedEncodingError: ('Connection broken: OSError("(104, \'ECONNRESET\')",)', OSError("(104, 'ECONNRESET'
)",))
During handling of the above exception, another exception occurred:

AttributeError                            Traceback (most recent call last)
/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py in showtraceback(self, exc_tuple, filename, tb_offset, exception_only, running_compiled_code)
   1827                         # in the engines. This should return a list of strings.
-> 1828                         stb = value._render_traceback_()
   1829                     except Exception:

AttributeError: 'ChunkedEncodingError' object has no attribute '_render_traceback_'

During handling of the above exception, another exception occurred:

TypeError                                 Traceback (most recent call last)
/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py in run_code(self, code_obj, result)
   2925             if result is not None:
   2926                 result.error_in_exec = sys.exc_info()[1]
-> 2927             self.showtraceback(running_compiled_code=True)
   2928         else:
   2929             outflag = False

/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py in showtraceback(self, exc_tuple, filename, tb_offset, exception_only, running_compiled_code)
   1829                     except Exception:
   1830                         stb = self.InteractiveTB.structured_traceback(etype,
-> 1831                                             value, tb, tb_offset=tb_offset)
   1832
   1833                     self._showtraceback(etype, value, stb)

/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py in structured_traceback(self, etype, value, tb, tb_offset, number_of_lines_of_context)
   1369         self.tb = tb
   1370         return FormattedTB.structured_traceback(
-> 1371             self, etype, value, tb, tb_offset, number_of_lines_of_context)
   1372
   1373

/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py in structured_traceback(self, etype, value, tb, tb_offset, number_of_lines_of_context)
   1277             # Verbose modes need a full traceback
   1278             return VerboseTB.structured_traceback(
-> 1279                 self, etype, value, tb, tb_offset, number_of_lines_of_context
   1280             )
   1281         else:

/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py in structured_traceback(self, etype, evalue, etb, tb_offset, number_of_lines_of_context)
   1138             exception = self.get_parts_of_chained_exception(evalue)
   1139             if exception:
-> 1140                 formatted_exceptions += self.prepare_chained_exception_message(evalue.__cause__)
   1141                 etype, evalue, etb = exception
   1142             else:

TypeError: Can't convert 'list' object to str implicitly
