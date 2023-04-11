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


def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]
def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
def download():
    products_data = pd.read_csv(r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\vatly24h\hoc24hurl\vatly247.csv')
    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(20)

    #list_link = to_dowload.loc[to_dowload['download'] != 'Die']
    test_link = ['https://vatly247.com/dao-dong-va-song-dien-tu-a291.html']
    # test_link = []
    # test_link = []
    for link in tqdm(list_link):
        req = requests.get(link)
        page_source = req.text
        sleep(2)
        soup =BeautifulSoup(page_source,'lxml')
        element = soup.find('body')
        check_download = element.find('button', class_="btn_gray")
        subject_Name = element.find('span',class_="fl").text
        lecture = element.find('a', class_="clblue").text

        #local = soup.find('ul', class_="tlmenu")
        if check_download == None:
            print(0)
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\vatly24h\hoc24hurl\vatly247.csv")
            continue
        else:
            url_local = check_download['onclick']
            url = Find(url_local)[0]
            print(url)
            pass

        dowload_url = url
        newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\vatly24h\download/' + subject_Name
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        download_dir = newpath.replace('/', '\\')

        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2,
                 "download.default_directory": download_dir,
                 "download.prompt_for_download": False}

        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        options.add_argument("log-level=3")
        # options.add_argument('--headless')
        browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
        browser.get(dowload_url)
        paths = WebDriverWait(browser, 60, 1).until(every_downloads_chrome)
        print(paths)
        print('finish!')
        browser.delete_all_cookies()
        #browser.quit()

        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\vatly24h\hoc24hurl\vatly247.csv")
download()