#https://pypi.org/project/facebook-scraper/

from facebook_scraper import get_posts
import pandas as pd

data = get_posts(group='chomuabanphukiendienthoai', pages=1)

data = pd.DataFrame.from_dict(data)

data.to_csv('Fb_page.csv', index=False)