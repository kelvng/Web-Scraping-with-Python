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

def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]
def download():
    products_data = pd.read_csv(r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\giaovienvn\giaovienurl\giaovinevn1.csv')
    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(20)

    test_link = ['https://giaovienvietnam.com/dot-bien-cau-truc-nhiem-sac-the-nst-di-truyen-hoc-sinh-hoc-12/','https://giaovienvietnam.com/download/nhung-bai-cam-thu-van-hoc-lop-4/','https://giaovienvietnam.com/download/on-tap-cuoi-ki-2-mon-toan-lop-4/']
    for link in tqdm(list_link):
        print(1)
        req = requests.get(link)
        page_source =req.text
        soup =BeautifulSoup(page_source,'lxml')
        print(soup.find('div', class_="ml-3"))
        if soup.find('div', class_="ml-3") == None:
            print('pass')
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(
                r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\giaovienvn\giaovienurl\giaovinevn1.csv")
            continue
        else:
            print('contiue download')
            pass
        #phân loại
        local = soup.find('div', class_="breadcrumb")
        print(local)
        name_local = local.find_all('a')
        print(name_local)
        print(len(name_local))
        if len(name_local) == 5 :
            class_name = name_local[2].text
            path = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\giaovienvn\Download/'+ class_name
            if not os.path.exists(path):
                os.makedirs(path)
            big_folder = name_local[3].text
            small_folder = name_local[4].text
            newpath = path + '/' + big_folder + '/' + small_folder
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            pass
        elif len(name_local) == 4:
            class_name = name_local[2].text
            big_folder = name_local[3].text
            newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\giaovienvn\Download/'+class_name +'/'+ big_folder
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            pass
        elif len(name_local) == 2:
            big_folder = name_local[1].text
            newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\giaovienvn\Download/' + big_folder
            if not os.path.exists(newpath):
                os.makedirs(newpath)
        else:
            class_name = name_local[2].text
            newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\giaovienvn\Download/' + class_name
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            print('check!')
            pass
        download_dir = newpath.replace('/', '\\')
        link_local = soup.find('div', class_="ml-3")
        print(link_local)
        url = link_local.find('a')['onclick']
        url = Find(url)[0].replace("';return",'')
        print(url)
        req =requests.get(url)
        req =req.text
        soup = BeautifulSoup(req,'lxml')
        link_local = soup.find('td', class_='text-right')
        url = link_local.find('a')['href']
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2,
                 "download.default_directory": download_dir,
                 "download.prompt_for_download": False}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        options.add_argument("log-level=3")
        options.add_argument("user-data-dir=C:\\Users\\Admin 3i\\AppData\Local\\Google\\Chrome\\User Data\\Profile 8")
        # options.add_argument('--headless')
        browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)
        browser.get(url)
        sleep(1)
        #browser.find_element_by_xpath('//*[@class="white-space: nowrap;"]').click()
        sleep(4)
        browser.delete_all_cookies()
        browser.quit()
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(
            r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\giaovienvn\giaovienurl\giaovinevn1.csv")

download()

