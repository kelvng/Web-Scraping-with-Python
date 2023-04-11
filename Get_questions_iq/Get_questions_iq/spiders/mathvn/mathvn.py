import requests
import selenium
import json
import time
from datetime import datetime
import time
import csv
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
path1 = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\mathvn\url\ggmathvn.csv'
products_data = pd.read_csv(path1)
#products_data['download'] = np.nan
# products_data['time_scan'] = np.nan
list_link = products_data.loc[products_data['download'] != 'Yes']
list_link = list_link.loc[list_link['download'] != 'Die']['link']
options = webdriver.ChromeOptions()
download_dir = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\mathvn\Downlaod\drivegoogle'
prefs = {"profile.default_content_setting_values.notifications": 2,
         "download.default_directory": download_dir,
         "download.prompt_for_download": False}

options.add_experimental_option("prefs", prefs)
options.add_argument("--start-maximized")
options.add_argument("log-level=3")
#options.add_argument('--headless')
#options.add_argument(
#    "user-data-dir=C:\\Users\\Admin 3i\\AppData\Local\\Google\\Chrome\\User Data\\Profile 8")
# browser = webdriver.Chrome(chrome_options=options)
browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
test = ['http://www.mediafire.com/?ymcyx400tyy','http://www.mediafire.com/?jgngozgbwmc']
def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

for url in tqdm(list_link):
    download_url = url+
    browser.get()

