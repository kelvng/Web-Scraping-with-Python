# Tổng 3004
#Tổng 7523
import json
import time
from datetime import datetime
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = document.querySelector('downloads-manager')
            .shadowRoot.getElementById('downloadsList').items;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)
path1 = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\THCStoanmath\url\thcs_toanmath.csv'
def download():
    products_data = pd.read_csv(path1)
    # products_data['download'] = np.nan
    # products_data['time_scan'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(50)
    link = ['https://thcs.toanmath.com/2022/05/de-hoc-ki-2-toan-7-nam-2021-2022-phong-gddt-thanh-pho-ninh-binh.html','https://thcs.toanmath.com/2017/12/de-kiem-tra-hk1-toan-7-nam-hoc-2017-2018-phong-gd-va-dt-nam-truc-nam-dinh.html']
    for url in tqdm(list_link):
        req = requests.get(url)
        start_time = time.time()

        page_source = req.text
        soup =BeautifulSoup(page_source, 'lxml')

        if soup.find('button', class_="pdf-download") == None:
            #productdata = 'DIE'
            products_data.loc[products_data['link'] == url, 'download'] = 'Die'
            products_data.to_csv(path1, index= False)

            continue
        else:
            title = soup.find('h1').text
            check_class = soup.find('span', class_="entry-meta-categories").text
            print(title)
            print(check_class)
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\THCStoanmath\Download/'
            #foldersoft
            if '7' in title or '7' in check_class and '':
                newpath = path + 'Lớp 7'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                if 'de-' in url or 'trac-nghiem' in url or 'on-thi' in url or 'bi-kip' in url:
                    newpath = newpath + '/' + 'đề thi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                elif 'bai-tap' in url or 'tai-lieu' in url:
                    newpath = newpath + '/' + 'baigiang_dethi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                else:
                    newpath = newpath + '/' + 'baigiang'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
            elif '6' in title or '6' in check_class:
                newpath = path + 'Lop 6'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                if 'de-' in url or 'trac-nghiem' in url or 'on-thi' in url or 'bi-kip' in url:
                    newpath = newpath + '/' + 'đề thi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                elif 'bai-tap' in url or 'tai-lieu' in url:
                    newpath = newpath + '/' + 'baigiang_dethi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                else:
                    newpath = newpath + '/' + 'baigiang'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
            elif '8' in title or '8' in check_class:
                newpath = path + 'Lớp 8'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                if 'de-' in url or 'trac-nghiem' in url or 'on-thi' in url or 'bi-kip' in url:
                    newpath = newpath + '/' + 'đề thi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                elif 'bai-tap' in url or 'tai-lieu' in url:
                    newpath = newpath + '/' + 'baigiang_dethi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                else:
                    newpath = newpath + '/' + 'baigiang'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
            elif '9' in title or '9' in check_class or 'lop-10' in url:
                newpath = path + 'Lớp 9'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                if 'de-' in url or 'trac-nghiem' in url or 'on-thi' in url or 'bi-kip' in url:
                    newpath = newpath + '/' + 'đề thi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                elif 'bai-tap' in url or 'tai-lieu' in url:
                    newpath = newpath + '/' + 'baigiang_dethi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                else:
                    newpath = newpath + '/' + 'baigiang'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
            elif 'quan-6' in url or 'quan-7' in url or 'quan-8' in url or 'quan-9' in url:
                newpath = path + 'class'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                if 'de-' in url or 'trac-nghiem' in url or 'on-thi' in url or 'bi-kip' in url:
                    newpath = newpath + '/' + 'đề thi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                elif 'bai-tap' in url or 'tai-lieu' in url:
                    newpath = newpath + '/' + 'baigiang_dethi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                else:
                    newpath = newpath + '/' + 'baigiang'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
            else:
                # check new folder for this
                print('cant fill class')
                newpath = path + 'class'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                if 'de-' in url or 'trac-nghiem' in url or 'on-thi' in url or 'bi-kip' in url:
                    newpath = newpath + '/' + 'đề thi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                elif 'bai-tap' in url or 'tai-lieu' in url:
                    newpath = newpath + '/' + 'baigiang_dethi'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                else:
                    newpath = newpath + '/' + 'baigiang'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
            download_dir = newpath.replace('/', '\\')

            # check link
            pass
            options = webdriver.ChromeOptions()

            prefs = {"profile.default_content_setting_values.notifications": 2,
                     "download.default_directory": download_dir,
                     "download.prompt_for_download": False}

            options.add_experimental_option("prefs", prefs)
            options.add_argument("--start-maximized")
            options.add_argument("log-level=3")
            # options.add_argument('--headless')
            #options.add_argument(
            #    "user-data-dir=C:\\Users\\Admin 3i\\AppData\Local\\Google\\Chrome\\User Data\\Profile 8")
            # browser = webdriver.Chrome(chrome_options=options)
            browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
            browser.get(url)
            try:
                browser.find_element_by_partial_link_text('TẢI XUỐNG').click()
                print('word')
            except:
                print(1)
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@class="pdf-download"]').click()
            print('pdf')
            paths = WebDriverWait(browser, 60, 1).until(every_downloads_chrome)
            print(paths)
            browser.delete_all_cookies()
            browser.quit()
            products_data.loc[products_data['link'] == url, 'download'] = 'Yes'
            products_data.to_csv(path1, index=False)
            time_scan = str(time.time()-start_time)
            products_data.loc[products_data['link'] == url, 'time_scan'] = time_scan
            products_data.to_csv(path1, index= False)


download()
