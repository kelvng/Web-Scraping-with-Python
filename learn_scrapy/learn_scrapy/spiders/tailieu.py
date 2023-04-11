import pandas as pd


from bs4 import BeautifulSoup as bs

import requests

from bs4 import BeautifulSoup

import lxml

soup = BeautifulSoup (open("test.csv", encoding="utf8"), features="lxml")

links = soup.find_all('a')

for link in links:
    print(link['href'])