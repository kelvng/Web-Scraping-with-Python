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
DownloadLst = []
def download():
    products_data = pd.read_csv(r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tailieuGVvietnam\Url\www.tailieugiaoviendeep=6.csv')
    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link']

    #list_link = to_dowload.loc[to_dowload['download'] != 'Die']
    test_link = ['https://www.tailieugiaovien.com/2021/08/giao-an-toan-6-7-8-9-10-11-12-cv-5512.html','https://www.tailieugiaovien.com/2021/08/giao-an-sinh-hoc-cv-5512-lop-6-7-8-9-10-11-12.html']
    # test_link = []
    # test_link = []
    for link in tqdm(list_link):
        req = requests.get(link)
        page_source = req.text
        sleep(2)
        soup =BeautifulSoup(page_source,'lxml')
        element = soup.find('body')
        dowload_list = element.find_all('a', class_="button medium demo")
        check_download = element.find('a', class_="button medium demo")
        if check_download == None:
            print(0)
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tailieuGVvietnam\Url\www.tailieugiaoviendeep=6.csv")

            continue
        else:
            pass
        #DownloadLst = []
        for i in dowload_list:
            Url = i['href']
            if Url != '#':
                DownloadLst.append(i['href'])
        print(DownloadLst)
        # newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tailieuGVvietnam\download'
        # if not os.path.exists(newpath):
        #     os.makedirs(newpath)
        #
        # download_dir = newpath
        # # login
        # options = webdriver.ChromeOptions()
        # prefs = {"profile.default_content_setting_values.notifications": 2,
        #          "download.default_directory": download_dir,
        #          "download.prompt_for_download": False}
        #
        # options.add_experimental_option("prefs", prefs)
        # options.add_argument("--start-maximized")
        # options.add_argument("log-level=3")
        # # options.add_argument('--headless')
        # browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
        # browser.get(dowload_url)
        # sleep(2)
        # browser.find_element_by_xpath('//*[@title="Download"]').click()
        # sleep(2)
        # browser.find_element_by_xpath('//*[@title="Download"]').click()
        # sleep(3)
        # paths = WebDriverWait(browser, 60, 1).until(every_downloads_chrome)
        # print(paths)
        # print('finish!')
        # # browser.delete_all_cookies()
        # # browser.quit()
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tailieuGVvietnam\Url\www.tailieugiaoviendeep=6.csv")
download()
filename = 'ggdrive'
with open(filename +'.csv', 'w', newline='', encoding="utf-8") as file_output:
    headers = ['link']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
    writer.writeheader()
    # print(URLs_all_page)
    for value in DownloadLst:

        writer.writerow({headers[0]: value})