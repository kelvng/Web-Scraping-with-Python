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
List_onedirve = []
def download():
    products_data = pd.read_csv(r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Giaotrinhhay\url\giaotrinhhay.csv')
    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(50)

    #list_link = to_dowload.loc[to_dowload['download'] != 'Die']
    test_link = ['https://giaotrinhhay.com/tai-lieu-hoc-tieng-trung/','https://giaotrinhhay.com/tai-lieu-hoc-tieng-anh/']
    # test_link = []
    # test_link = []
    for link in tqdm(list_link):
        try:
            req = requests.get(link)
            page_source = req.text
        except:
            continue
        soup =BeautifulSoup(page_source,'lxml')
        element = soup.find('body')
        try:

            local_url = element.find('div', class_="post-inner")
            PostLink = local_url.find_all('a')

            Lst = []
            for i in PostLink:
                Url = i['href']
                if 'drive.google' in Url or 'mdedifire' in Url or 'fshare' in Url:
                    Lst.append(Url)
            products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Giaotrinhhay\url\giaotrinhhay.csv")
            pass
        except:
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Giaotrinhhay\url\giaotrinhhay.csv")
            continue


        filename = 'giaotrinhhay'
        myUUID = uuid.uuid4()
        if len(Lst) != 0:
            with open(filename + str(myUUID) + '.csv', 'w', newline='', encoding="utf-8") as file_output:
                headers = ['link']
                writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
                writer.writeheader()
                for value in Lst:
                    writer.writerow({headers[0]: value})

download()


