import csv
import json
import os
import re
from datetime import datetime
#VIP.
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

def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)


path1 = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\thuvienhoclieu\Urrl\demodowload2.csv'
# browser.get(url)
# sleep(2)
products_data = pd.read_csv(path1)
#products_data['download'] = np.nan
list_link = products_data.loc[products_data['download'] != 'Yes']
list_link = list_link.loc[list_link['download'] != 'Die']['link']
url = ['https://thuvienhoclieu.com/60-cau-hoi-trac-nghiem-bai-phan-xa-toan-phan-co-dap/','https://thuvienhoclieu.com/tai-lieu-hoa-hoc/tai-lieu-hoa-hoc-lop-10/','https://thuvienhoclieu.com/phuong-phap-giai-toan-phan-ung-hat-nhan/']
for link in tqdm(list_link):
    print(link)
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}

    options.add_experimental_option("prefs", prefs)
    options.add_argument("--start-maximized")
    options.add_argument("log-level=3")
    options.add_argument('--headless')
    browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
    #req = requests.get(link)
    try:
        browser.get(link)
        sleep(1)
    except:
        browser.get(link)
        sleep(1)
    source = browser.page_source
    soup = BeautifulSoup(source,'lxml')
    #print(soup)

    check = soup.find('p', class_="embed_download")
    if check != None:
        local = soup.find('ul', class_="td-category")
        #print(local)
        try:
            subject = local.find_all('li')[1].text
        except:
            subject = local.find_all('li')[0].text
        lecture = soup.find('h1').text
        link_download = check.find('a')['href']
        browser.delete_all_cookies()
        browser.quit()
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(path1, index=False)
    else:
        print('die')
        browser.delete_all_cookies()
        browser.quit()
        products_data.loc[products_data['link'] == link, 'download'] = 'Die'
        products_data.to_csv(path1, index=False)
        continue

    path_download = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\thuvienhoclieu\Download'
    newpath = path_download + '/'+subject
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    download_dir = newpath.replace('/', '\\')
    options = webdriver.ChromeOptions()
    print(download_dir)
    prefs = {"profile.default_content_setting_values.notifications": 2,
             "download.default_directory": download_dir,
             "download.prompt_for_download": False}

    options.add_experimental_option("prefs", prefs)
    options.add_argument("--start-maximized")
    options.add_argument("log-level=3")
    options.add_argument('--headless')
    # options.add_argument(
    #    "user-data-dir=C:\\Users\\Admin 3i\\AppData\Local\\Google\\Chrome\\User Data\\Profile 8")
    # browser = webdriver.Chrome(chrome_options=options)
    browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
    browser.get(link_download)
    try:
        paths = WebDriverWait(browser, 60, 1).until(every_downloads_chrome)
        print(paths)
    except:
        pass
    browser.delete_all_cookies()
    browser.quit()
