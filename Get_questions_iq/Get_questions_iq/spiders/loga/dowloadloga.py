import csv
import os
import random
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
    r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\logadethi.csv')
#products_data['download'] = np.nan
to_dowload = products_data.loc[products_data['download'] != 'Yes']
to_dowload = to_dowload.loc[to_dowload['download'] != 'checkagain']
list_link = to_dowload.loc[to_dowload['download'] != 'Die']['link']
data =[]
def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
#test_link =['https://loga.vn/LessonPlan/LoadLessonPlanContentByFilter?gradeID=10&subjectID=4&page=1']
for link in tqdm(list_link):
    req = requests.get(link, verify=False)
    req = req.text
    soup = BeautifulSoup(req, 'lxml')
    print(link)
    if soup.find('div', class_="doc-content") != None:
        place = soup.find('div', class_="doc-content")
    else:
        place = soup.find('body')
    place = place.find_all('h1', class_="document-card-title row")
    list_doc =[]
    for i in place:
        Lst =[]
        url = i.find('a')['href']
        if 'http' not in url:
            url = 'https://loga.vn/' + url
        else:
            url = url
        list_doc.append(url)
    print(list_doc)
    for j in tqdm(list_doc):
        if 'gradeID=12' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Download\turn31-08\Lớp 12\đề thi'
            # '''&subjectID=2''' '''=1 Toán/ =5 tieng anh/ =3 hoa hoc / =4 sinh hoc / =2 vat ly / =6 ngu van / =8 lich su/ =7 dia ly / =10 GDCD / =13 bang tin''''
            if 'subjectID=1' in link:
                namefolder = 'Toán'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=2' in link:
                namefolder = 'Vật lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=3' in link:
                namefolder = 'Hóa học'
                newpath = path + '/' + namefolder
                print(newpath)
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=4' in link:
                namefolder = 'sinh học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=5' in link:
                namefolder = 'Tiếng anh'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=6' in link:
                namefolder = 'Ngữ văn'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=7' in link:
                namefolder = 'Địa lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=8' in link:
                namefolder = 'Lịch sử'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=10' in link:
                namefolder = 'GDCD'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=13' in link:
                namefolder = 'Thủ thuật Tin'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
        if 'gradeID=11' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Download\turn31-08\Lớp 11\đề thi'
            # '''&subjectID=2''' '''=1 Toán/ =5 tieng anh/ =3 hoa hoc / =4 sinh hoc / =2 vat ly / =6 ngu van / =8 lich su/ =7 dia ly / =10 GDCD / =13 bang tin''''
            if 'subjectID=1' in link:
                namefolder = 'Toán'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=2' in link:
                namefolder = 'Vật lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=3' in link:
                namefolder = 'Hóa học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=4' in link:
                namefolder = 'sinh học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=5' in link:
                namefolder = 'Tiếng anh'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=6' in link:
                namefolder = 'Ngữ văn'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=7' in link:
                namefolder = 'Địa lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=8' in link:
                namefolder = 'Lịch sử'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=10' in link:
                namefolder = 'GDCD'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=13' in link:
                namefolder = 'Thủ thuật Tin'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
        if 'gradeID=10' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Download\turn31-08\Lớp 10\đề thi'
            # '''&subjectID=2''' '''=1 Toán/ =5 tieng anh/ =3 hoa hoc / =4 sinh hoc / =2 vat ly / =6 ngu van / =8 lich su/ =7 dia ly / =10 GDCD / =13 bang tin''''
            if 'subjectID=1' in link:
                namefolder = 'Toán'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=2' in link:
                namefolder = 'Vật lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=3' in link:
                namefolder = 'Hóa học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=4' in link:
                namefolder = 'sinh học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=5' in link:
                namefolder = 'Tiếng anh'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=6' in link:
                namefolder = 'Ngữ văn'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=7' in link:
                namefolder = 'Địa lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=8' in link:
                namefolder = 'Lịch sử'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=10' in link:
                namefolder = 'GDCD'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=13' in link:
                namefolder = 'Thủ thuật Tin'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
        if 'gradeID=9' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Download\turn31-08\Lớp 9\đề thi'
            # '''&subjectID=2''' '''=1 Toán/ =5 tieng anh/ =3 hoa hoc / =4 sinh hoc / =2 vat ly / =6 ngu van / =8 lich su/ =7 dia ly / =10 GDCD / =13 bang tin''''
            if 'subjectID=1' in link:
                namefolder = 'Toán'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=2' in link:
                namefolder = 'Vật lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=3' in link:
                namefolder = 'Hóa học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=4' in link:
                namefolder = 'sinh học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=5' in link:
                namefolder = 'Tiếng anh'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=6' in link:
                namefolder = 'Ngữ văn'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=7' in link:
                namefolder = 'Địa lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=8' in link:
                namefolder = 'Lịch sử'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=10' in link:
                namefolder = 'GDCD'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=13' in link:
                namefolder = 'Thủ thuật Tin'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
        if 'gradeID=8' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Download\turn31-08\Lớp 8\đề thi'
            # '''&subjectID=2''' '''=1 Toán/ =5 tieng anh/ =3 hoa hoc / =4 sinh hoc / =2 vat ly / =6 ngu van / =8 lich su/ =7 dia ly / =10 GDCD / =13 bang tin''''
            if 'subjectID=1' in link:
                namefolder = 'Toán'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=2' in link:
                namefolder = 'Vật lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=3' in link:
                namefolder = 'Hóa học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=4' in link:
                namefolder = 'sinh học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=5' in link:
                namefolder = 'Tiếng anh'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=6' in link:
                namefolder = 'Ngữ văn'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=7' in link:
                namefolder = 'Địa lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=8' in link:
                namefolder = 'Lịch sử'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=10' in link:
                namefolder = 'GDCD'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=13' in link:
                namefolder = 'Thủ thuật Tin'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
        if 'gradeID=7' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Download\turn31-08\Lớp 7\đề thi'
            # '''&subjectID=2''' '''=1 Toán/ =5 tieng anh/ =3 hoa hoc / =4 sinh hoc / =2 vat ly / =6 ngu van / =8 lich su/ =7 dia ly / =10 GDCD / =13 bang tin''''
            if 'subjectID=1' in link:
                namefolder = 'Toán'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=2' in link:
                namefolder = 'Vật lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=3' in link:
                namefolder = 'Hóa học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=4' in link:
                namefolder = 'sinh học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=5' in link:
                namefolder = 'Tiếng anh'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=6' in link:
                namefolder = 'Ngữ văn'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=7' in link:
                namefolder = 'Địa lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=8' in link:
                namefolder = 'Lịch sử'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=10' in link:
                namefolder = 'GDCD'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=13' in link:
                namefolder = 'Thủ thuật Tin'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
        if 'gradeID=6' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Download\turn31-08\Lớp 6\đề thi'
            # '''&subjectID=2''' '''=1 Toán/ =5 tieng anh/ =3 hoa hoc / =4 sinh hoc / =2 vat ly / =6 ngu van / =8 lich su/ =7 dia ly / =10 GDCD / =13 bang tin''''
            if 'subjectID=1' in link:
                namefolder = 'Toán'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=2' in link:
                namefolder = 'Vật lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=3' in link:
                namefolder = 'Hóa học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=4' in link:
                namefolder = 'sinh học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=5' in link:
                namefolder = 'Tiếng anh'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=6' in link:
                namefolder = 'Ngữ văn'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=7' in link:
                namefolder = 'Địa lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=8' in link:
                namefolder = 'Lịch sử'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=10' in link:
                namefolder = 'GDCD'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=13' in link:
                namefolder = 'Thủ thuật Tin'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
        if 'gradeID=15' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Download\turn31-08\Lớp 13+\đề thi'
            # '''&subjectID=2''' '''=1 Toán/ =5 tieng anh/ =3 hoa hoc / =4 sinh hoc / =2 vat ly / =6 ngu van / =8 lich su/ =7 dia ly / =10 GDCD / =13 bang tin''''
            if 'subjectID=1' in link:
                namefolder = 'Toán'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=2' in link:
                namefolder = 'Vật lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=3' in link:
                namefolder = 'Hóa học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=4' in link:
                namefolder = 'sinh học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=5' in link:
                namefolder = 'Tiếng anh'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=6' in link:
                namefolder = 'Ngữ văn'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=7' in link:
                namefolder = 'Địa lý'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=8' in link:
                namefolder = 'Lịch sử'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=10' in link:
                namefolder = 'GDCD'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=13' in link:
                namefolder = 'Thủ thuật Tin'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=28' in link:
                namefolder = 'Dạy học'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=27' in link:
                namefolder = 'Văn Phòng'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=29' in link:
                namefolder = 'Sức khỏe'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'subjectID=30' in link:
                namefolder = 'Bán hàng'
                newpath = path + '/' + namefolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
        download_dir = newpath.replace('/','\\')
        #browser
        options = webdriver.ChromeOptions()

        prefs = {"profile.default_content_setting_values.notifications": 2,
                 "download.default_directory": download_dir,
                 "download.prompt_for_download": False}

        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        options.add_argument("log-level=3")
        # options.add_argument('--headless')
        options.add_argument(r"user-data-dir=C:\Users\Server\AppData\Local\Google\Chrome\User Data\Profile 8")
        #browser = webdriver.Chrome(chrome_options=options)
        browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
        try:
            browser.get(j)
            sleep(1)
        except:
            browser.get(j)
            sleep(1)
        try:
            sleep(1)
            browser.find_element_by_xpath('//*[@class="btn btn-danger btnDownload center"]').click()
        except:
            print('hmm')
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\logadethi.csv")
            browser.delete_all_cookies()
            browser.quit()
            browser.close()
            continue

        sleep(2)
        #browser.find_element_by_xpath('/*[@class="glyphicon glyphicon-download-alt"]').click()
        browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/a').click()
        sleep(5)
        paths = WebDriverWait(browser, 120, 1).until(every_downloads_chrome)
        print(paths)
        print('finish!')
        browser.delete_all_cookies()
        browser.quit()
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(
            r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\logadethi.csv")