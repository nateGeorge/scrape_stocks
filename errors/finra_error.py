waiting for market to close, waiting 1 hour...
scraping...
ERROR:root:Internal Python error in the inspect module.
Below is the traceback from this internal error.

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py", line 2910, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-2-2c9937c17e38>", line 1, in <module>
    daily_scrape_data()
  File "/home/nate/github/scrape_stocks/scrape_finra_shorts.py", line 225, in daily_scrape_data
    update_data(check_all_months=True)
  File "/home/nate/github/scrape_stocks/scrape_finra_shorts.py", line 134, in update_data
    uls, month_links = get_idx(verbose=verbose)
  File "/home/nate/github/scrape_stocks/scrape_finra_shorts.py", line 98, in get_idx
    month_links = [t.attrs['href'] for t in tables[1].find_all('a')]
IndexError: list index out of range

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/interactiveshell.py", line 1828, in showtraceback
    stb = value._render_traceback_()
AttributeError: 'IndexError' object has no attribute '_render_traceback_'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py", line 1090, in get_records
    return _fixed_getinnerframes(etb, number_of_lines_of_context, tb_offset)
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py", line 311, in wrapped
    return f(*args, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/IPython/core/ultratb.py", line 345, in _fixed_getinnerframes
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
