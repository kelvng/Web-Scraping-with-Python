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


def download():
    products_data = pd.read_csv(
        r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Toanmath\url\downloadtoanmath.csv')
    # products_data['download'] = np.nan
    # products_data['time_scan'] = np.nan
    list_link = products_data.loc[products_data['download'] == 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(10)
    #link = ['https://thcs.toanmath.com/2022/05/de-hoc-ki-2-toan-7-nam-2021-2022-phong-gddt-thanh-pho-ninh-binh.html','https://toanmath.com/2017/06/bai-tap-trac-nghiem-hinh-hoc-khong-gian-le-viet-nhon.html']
    for url in tqdm(list_link):
        req = requests.get(url)
        start_time = time.time()

        page_source = req.text
        soup =BeautifulSoup(page_source, 'lxml')

        if soup.find('button', class_="pdf-download") == None:
            #productdata = 'DIE'
            products_data.loc[products_data['link'] == url, 'download'] = 'Die'
            products_data.to_csv(
                r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Toanmath\url\downloadtoanmath.csv', index=False)

            continue
        else:
            title = soup.find('h1').text
            check_class = soup.find('span', class_="entry-meta-categories").text
            print(title)
            print(check_class)
            path = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Toanmath\Download/'
            #foldersoft
            if '11' in title or '11' in check_class:
                newpath = path + 'Lớp_11'
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
            elif '12' in title or '12' in check_class or 'THPT' in title or 'THPT' in check_class:
                newpath = path + 'Lop_12'
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
            elif '10' in title or '10' in check_class:
                newpath = path + 'Lớp_10'
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
            download_dir = newpath.replace('/','\\')

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
            options.add_argument(
                "user-data-dir=C:\\Users\\Admin 3i\\AppData\Local\\Google\\Chrome\\User Data\\Profile 8")
            # browser = webdriver.Chrome(chrome_options=options)
            browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)
            browser.get(url)
            try:
                browser.find_element_by_partial_link_text('TẢI XUỐNG').click()
                print('word')
            except:
                print(1)
                pass
            time.sleep(2)
            browser.find_element_by_xpath('//*[@class="pdf-download"]').click()

            time.sleep(5)
            browser.delete_all_cookies()
            browser.quit()
            products_data.loc[products_data['link'] == url, 'download'] = 'Yes'
            products_data.to_csv(
                r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Toanmath\url\downloadtoanmath.csv', index=False)
            time_scan = str(time.time()-start_time)
            products_data.loc[products_data['link'] == url, 'time_scan'] = time_scan
            products_data.to_csv(
                r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Toanmath\url\downloadtoanmath.csv', index=False)


download()
