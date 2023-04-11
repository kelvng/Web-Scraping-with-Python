#https://pypi.org/project/youtube-comment-scraper-python/
import json

import csvfile as csvfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd
import numpy as np
from youtube_comment_scraper_python import *

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome('../../../chromedriver97.exe', options=options)
youtube.open("https://www.youtube.com/watch?v=z-WrP9M8yzY")
response=youtube.video_comments()
data=response['body']
print(data)