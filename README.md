# scrape_stocks
Scrapes short interest and historical daily prices for US stocks.

All done on Ubuntu 16.04 64-bit.

# Getting it running
## Install requirements
`sudo pip3 install -r requirements.txt`

## Install mongodb and start it
https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04

## scrape
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
