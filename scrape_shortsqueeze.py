# would need to use selenium to get this to work...meh, just use a multidownloader for chrome

import requests as req
from bs4 import BeautifulSoup as bs

base_url = 'http://shortsqueeze.com/{}.php'

years = ['2015', '2016', '2017']

for y in years:
    url = base_url.format(y)
    res = req.get(url)
    soup = bs(res.content, 'lxml')
    soup.find_all({'class': 'hyper13'})
