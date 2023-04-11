import csv
import os
import re

import numpy as np
from pywinauto import Application
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import scrapy
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup as BSHTML
import uuid
from tqdm import tqdm
from docx import Document
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

products_data = pd.read_csv(
    r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\stem-steam\alldrive\stemsteamggdrive.csv')
products_data['download'] = np.nan
list_link = products_data.loc[products_data['download'] != 'Yes']
list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(4000)

download_dir = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\stem-steam\Download'
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2,
         "download.default_directory": download_dir,
         "download.prompt_for_download": False}

options.add_experimental_option("prefs", prefs)
options.add_argument("--start-maximized")
options.add_argument("log-level=3")
def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
for link in tqdm(list_link):

    # # login

    # options.add_argument('--headless')
    browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
    browser.get(link)
    sleep(2)

    paths = WebDriverWait(browser, 60, 1).until(every_downloads_chrome)
    print(paths)
    print('finish!')
    browser.delete_all_cookies()
    browser.close()
    browser.quit()
    products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
    products_data.to_csv(
        r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\stem-steam\url\thuvienstem-steamcomdeep=6.csv")