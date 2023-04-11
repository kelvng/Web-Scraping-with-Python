import csv
from hashlib import new

from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.chrome import webdriver
from tqdm import tqdm
import json

import csvfile as csvfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd
import numpy as np
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome(executable_path=r'C:\Users\pycha\PycharmProjects\Source\chromedriver97.exe', options=options)

class url_obj:
    def __init__(self, url, iscan, deep):
        self.url = url
        self.iscan = iscan
        self.deep = deep
# creating list
browser.get("https://fptshop.com.vn/")
page_source = browser.page_source
soup = bs(page_source, 'lxml')
list_child_url = []
list_child_url.append( url_obj('Akash', 0, 1))
    # tìm tất cả đường link của các group
page_groups = soup.find("html")
url_obj_tpm = new
url_obj
n = 1
t = 0
v =0
for s in page_groups.find_all('a'):
        try:
                link = s['href']
                link = 'https://vneconomy.vn'+link
                t =0;
                for obj in list:
                    if (obj.url == link):
                        t =1;
                    else:
                        pass
                if t == 0:
                    url = link
                    iscan = 0
                    deep = n + 1
                    list_child_url.append(url_obj(url, iscan, deep))
        except:
            pass

for obj in list_child_url:
    print(obj.url, obj.iscan, obj.deep, sep=' ')
print(len(list_child_url))
# crawl_link (url_cur,n)
print(list_child_url)
browser.close()

