import pandas as pd

from utils import get_home_dir

HOME_DIR = get_home_dir(repo_name='scrape_stocks')

# free one from usfundamentals.com
df = pd.read_csv(HOME_DIR + 'data/usfundamentals/latest-snapshot-quarterly.csv')

# free one from sharadar
df = pd.read_csv(HOME_DIR + 'data/sharadar_fundamentals/SF0_20180321.csv')
