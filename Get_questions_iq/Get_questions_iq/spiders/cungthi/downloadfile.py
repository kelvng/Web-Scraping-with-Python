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

def download():
    products_data = pd.read_csv(r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\cungthi247url\chitiet.csv')
    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] == 'No']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(1)

    #list_link = to_dowload.loc[to_dowload['download'] != 'Die']
   # test_link = []
    # test_link = []
    for link in tqdm(list_link):
        print(1)
        req = requests.get(link)
        page_source = req.text
        sleep(2)
        soup =BeautifulSoup(page_source,'lxml')

        title_local =soup.find('ul', class_="breadcrumb")
        title_local = title_local.find_all('li', class_="active")
        bigfolder = title_local[1].text
        bigfolder = bigfolder.replace(' ','')
        bigfolder = bigfolder.replace('\n','')
        smallfolder =title_local[2].text
        smallfolder = smallfolder.replace(' ','')
        smallfolder = smallfolder.replace('\n','')
        newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Download\cungthi/' + bigfolder + '/' + smallfolder
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        download_dir=newpath.replace('/','\\')
        url = soup.find('a', class_="btn btn-lg mt-xs btn-warning fa fa-download color-ececec")
        url = url['href']
        print(url)
        req =requests.get(url, verify=False)
        req =req.text
        soup=BeautifulSoup(req,'lxml')
        url = soup.find('a', class_="btn btn-lg mt-xs btn-success fa fa-download color-ececec")['href']
        print(url)
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2,
                 "download.default_directory": download_dir,
                 "download.prompt_for_download": False}

        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        options.add_argument("log-level=3")
        #options.add_argument('--headless')
        browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)
        browser.get(url)
        sleep(15)
        try:
            '''<input type="submit" id="uc-download-link" class="goog-inline-block jfk-button jfk-button-action" value="Download anyway">'''
            browser.find_element_by_xpath('//*[@id="uc-download-link"]').click()
        except:
            pass
        browser.delete_all_cookies()
        browser.quit()
        products_data.loc[products_data['link'] == link, 'download'] = 'No  '
        products_data.to_csv(r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\cungthi247url\chitiet.csv")



download()