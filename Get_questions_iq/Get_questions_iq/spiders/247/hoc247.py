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
    products_data = pd.read_csv(r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\247url\hoc247tulieudownload.csv')
    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(20)

    #list_link = to_dowload.loc[to_dowload['download'] != 'Die']
    test_link = ['https://hoc247.net/tu-lieu/lop-12/de-thi-online-thpt-qg-2018-mon-vat-ly-de-minh-hoa-bo-gddt-doc2637.html']
    # test_link = []
    # test_link = []
    for link in tqdm(list_link):
        req = requests.get(link)
        page_source = req.text
        sleep(2)
        soup =BeautifulSoup(page_source,'lxml')
        local = soup.find('ul', class_="tlmenu")
        if soup.find('span', class_="i-download") == None:
            print(0)
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(
                r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\247url\hoc247tulieudownload.csv")

            continue
        else:
            pass
        place_lst = local.find_all('li')
        for i in place_lst:
            if 'class="act"' in str(i):
                bigfolder = i.text
                bigfolder = bigfolder.replace('\n', '')
                print(bigfolder)
        local = soup.find('div', class_="breadcrum hidden-xs")
        place_lst = local.find_all('span')
        smallfolder = place_lst[2].text
        print(smallfolder)
        newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\hoc247net/' + bigfolder + '/' + smallfolder
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        download_dir = newpath.replace('/', '\\')
        payload = {'txtLoginUsername': 'huynguyen104798@gmail.com', 'txtLoginPassword': 'nguyenvanhuy'}
        with requests.Session() as session:
            post = session.post("https://hoc247.net/tai-khoan/dang-nhap.html", data=payload, verify=False)
            req = session.get(link)
        req = req.text
        soup = BeautifulSoup(req, 'lxml')
        url = soup.find('a', class_="btn btn-lg btn-download")['href']
        # login
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2,
                 "download.default_directory": download_dir,
                 "download.prompt_for_download": False}

        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        options.add_argument("log-level=3")
        # options.add_argument('--headless')
        browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)
        browser.get('https://hoc247.net/tai-khoan/dang-nhap.html')
        sleep(1)
        try:
            browser.find_element_by_xpath('//*[@class="close-abs"]').click()
        except:
            pass
        user = browser.find_element_by_xpath('//*[@id="txtLoginUsername"]')
        user.send_keys('huynguyen104798@gmail.com')
        password = browser.find_element_by_xpath('//*[@id="txtLoginPassword"]')
        password.send_keys('nguyenvanhuy')
        browser.find_element_by_xpath('//*[@class="btn_blue_sm fleft hidden-xs visible-md visible-lg"]').click()
        sleep(1)
        browser.get(url)
        sleep(3)
        browser.delete_all_cookies()
        browser.quit()
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\247url\hoc247tulieudownload.csv")
download()