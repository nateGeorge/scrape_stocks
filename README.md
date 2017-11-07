# scrape_stocks
Scrapes short interest and historical daily prices for US stocks.

All done on Ubuntu 16.04 64-bit.

Currently getting data from FINRA, BATS

TODO: need to get data from here: ftp://ftp.nasdaqtrader.com/files/shortsaledata/daily/
 - maybe want to start getting key stats from here: https://stackoverflow.com/questions/38567661/how-to-get-key-statistics-for-yahoo-finance-web-search-api
 but need to write new parsing function

# Getting it running
## Install requirements
`sudo pip3 install -r requirements.txt`

## Install mongodb and start it
https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04

## scrape
To do a basic scrape, do:
```python
run scrape_stockdata.py
tickers = get_stock_list(scrape=False)
tickers = get_yahoo_tickers(tickers)
df = scrape_all_tickers(tickers)
```

```python
run scrape_stockdata.py
tickers = get_stock_list(no_scrape=True)
tickers = get_yahoo_tickers(tickers)
num_chunks = 90
tik = np.array(tickers)
chunk_size = tik.shape[0] // num_chunks
tiks = list(np.split(tik[:num_chunks * chunk_size], num_chunks))
if chunk_size != tik.shape[0] / num_chunks:
    tiks.append(tik[chunk_size * num_chunks:])

scrape_all_tickers_mongo(tiks[0][:5])

client = MongoClient()
db = client[DB]
coll = db['yahoo_stock_stats']
df = odo.odo(coll, pd.DataFrame)
client.close()
```
