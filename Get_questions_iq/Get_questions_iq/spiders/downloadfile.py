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
    products_data = pd.read_csv(r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\cungthi247url\chitiet.csv')
    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] == 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link']

    #list_link = to_dowload.loc[to_dowload['download'] != 'Die']
    test_link = ['https://hoc247.net/tu-lieu/lop-12/de-thi-online-thpt-qg-2018-mon-vat-ly-de-minh-hoa-bo-gddt-doc2637.html']
    # test_link = []
    # test_link = []
    for link in tqdm(test_link):
        print(1)
        req = requests.get(link)
        page_source = req.text
        sleep(2)
        soup =BeautifulSoup(page_source,'lxml')
        print(soup.find('span', class_="py-2 px-3"))
        #_____selector___hocmai.vn____
        if soup.find('div', class_="lib-sidebar") != None :
            try:
                local = soup.find('div', class_="breadcrumbs")
                title_local = local.find_all('a')
                folder_name = title_local[2].text

            except:
                continue

                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hocmaivn\Download/' + folder_name
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                download_dir= newpath.replace('/','\\')
                print(download_dir)
                #____________Slector
                download = soup.find('div', class_="download")
                url = download.find('a')['href']
                if 'https' not in url:
                    url = 'https://hocmai.vn' + url
                else:
                    url = url
                print(url)
                #_______Selector

                options = webdriver.ChromeOptions()
                prefs = {"profile.default_content_setting_values.notifications": 2,
                         "download.default_directory": download_dir,
                         "download.prompt_for_download": False}

                options.add_experimental_option("prefs", prefs)
                options.add_argument("--start-maximized")
                options.add_argument("log-level=3")
                #options.add_argument('--headless')
                browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)
                #________selector
                browser.get("https://hocmai.vn/")
                wait = WebDriverWait(browser, 1)
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn-acc btn-login"]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys("huynguyen104798@gmail.com")
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys("stop-pillo")
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="submit register-btn"]'))).click()
                #__________selector
                sleep(2)
                browser.get(url)
                sleep(3)
                browser.delete_all_cookies()
                browser.quit()
            products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
            products_data.to_csv(
                r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hocmaivn\hocmaiURL\download.csv")

            pass

        #_________sinhhoc247___________

        elif soup.find('button', class_='btn_gray') != None and 'sinhhoc247' in link:
            title = soup.find('div', class_="tab clearfix")
            bigfolder = title.find('span', class_="fl").text
            print(bigfolder)
            small = title.find_all('div', class_="sub")
            print(small)
            mediumfolder = small[0].text.replace(':', '')
            mediumfolder = mediumfolder.replace('  ', '')
            mediumfolder = mediumfolder.replace(' ', '')
            print(mediumfolder)
            smallfolder = small[1].text.replace(':', '')
            smallfolder = smallfolder.replace('  ', '')
            smallfolder = smallfolder.replace(' ', '')
            print(smallfolder)
            if 'Sinh học lớp 10' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Sinh học lớp 10/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            elif 'Sinh học lớp 9' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Sinh học lớp 9/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            elif 'Sinh học lớp 11' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Sinh học lớp 11/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            elif 'Sinh học lớp 12' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Sinh học lớp 12/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            else:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Sinhhoc'
            download_dir = newpath.replace('/', '\\')
            print(download_dir)
            products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
            products_data.to_csv(
                r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\247url\sinhoc247.csv")
            url = soup.find('button', class_="btn_gray")
            url = url['onclick']
            print(Find(url))
            options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2,
                     "download.default_directory": download_dir,
                     "download.prompt_for_download": False}
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--start-maximized")
            options.add_argument("log-level=3")
            # options.add_argument('--headless')
            browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)

            url = Find(url)[0]
            browser.get(url)
            sleep(10)
            browser.delete_all_cookies()
            browser.quit()

        # _________toanhoc247___________
        elif soup.find('button', class_="pdf-download") != None and 'toanhoc247' in link:
            title = soup.find('div', class_="tab clearfix")
            bigfolder = title.find('span', class_="fl").text
            print(bigfolder)
            small = title.find_all('div', class_="sub")
            print(small)
            mediumfolder = small[0].text.replace(':', '')
            mediumfolder = mediumfolder.replace('  ', '')
            mediumfolder = mediumfolder.replace(' ', '')
            print(mediumfolder)
            smallfolder = small[1].text.replace(':', '')
            smallfolder = smallfolder.replace('  ', '')
            smallfolder = smallfolder.replace(' ', '')
            print(smallfolder)
            if 'LỚP 6' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Toánlop6/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            if 'LỚP 7' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Toánlop7/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            elif 'LỚP 8' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Toánlop8/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            elif 'LỚP 9' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Toánlop9/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            elif 'LỚP 10' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Toánlop10/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            elif 'LỚP 11' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Toánlop11/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            elif 'LỚP 12' in bigfolder:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\toanlop12/' + mediumfolder + '/' + smallfolder
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
            else:
                newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\Toán'
            download_dir = newpath.replace('/', '\\')
            print(download_dir)
            products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
            products_data.to_csv(
                r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\247url\sinhoc247.csv")
            url = soup.find('button', class_="btn_gray")
            url = url['onclick']
            print(Find(url))
            #login
            options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2,
                     "download.default_directory": download_dir,
                     "download.prompt_for_download": False}
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--start-maximized")
            options.add_argument("log-level=3")
            # options.add_argument('--headless')
            browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)

            url = Find(url)[0]
            browser.get(url)
            sleep(2)
            browser.delete_all_cookies()
            browser.quit()
        #________123docz.net__________
        elif soup.find('span', class_="py-2 px-3") != None and '123docz' in link:
            # cant login with request.sesion useing selenium
            # payload = {'txtName': 'zetabase3i@gmail.com', 'txtPass': 'Langnghiem79'}
            # with requests.Session() as session:
            #     post = session.post("https://123docz.net/trang-chu.htm", data=payload, verify=False)
            #     req = session.get(link)

            title_local = soup.find_all('a', class_="cat_nav_top_a")

            bigfolder = title_local[0].text
            smallfolder =title_local[1].text
            newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\123docznet/' + bigfolder + '/' + smallfolder
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
            browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)
            #login

            wait = WebDriverWait(browser, 5)
            browser.get('https://123docz.net/trang-chu.htm')
            sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formLogin"]'))).click()
            sleep(0.5)
            user = browser.find_element_by_xpath('//*[@name="txtName"]')
            user.send_keys('zetabase3i@gmail.com')
            password = browser.find_element_by_xpath('//*[@name="txtPass"]')
            password.send_keys('Langnghiem79')
            browser.find_element_by_xpath('//*[@class="btn btn_login login-button"]').click()
            # wait = WebDriverWait(browser, 5)
            # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="py-2 px-3"]')))
            sleep(1)
            browser.get(link)
            sleep(2)
            price = browser.find_element_by_xpath('//*[@class="border border-gray-400 hidden md:block rounded pay_now_content"]').text
            print(price)
            if price == 'Giá: 0đ':
                browser.find_element_by_xpath('//*[@class="btn_download py-2 mr-2 hidden md:flex "]').click()
                wait = WebDriverWait(browser, 5)
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="btn btn_download flex font-bold h-12 items-center justify-center md:block md:h-8 md:text-base md:w-auto px-4 text-2xl w-1/2 down_now"]')))
                lst_download = browser.find_elements_by_xpath('//*[@class="btn btn_download flex font-bold h-12 items-center justify-center md:block md:h-8 md:text-base md:w-auto px-4 text-2xl w-1/2 down_now"]')
                for x in lst_download:
                    x.click()
                    sleep(1)
                sleep(2)
                browser.delete_all_cookies()
                browser.quit()
                products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
                products_data.to_csv(r"")
            else:
                products_data.loc[products_data['link'] == link, 'download'] = 'checkagain'
                products_data.to_csv(r"")
        #___________hoc247.net
        #quest request

        ## tài liệu
        elif soup.find('i', class_="fa fa-download hidden-xs") !=None and 'hoc247' in link:
            local = soup.find('ul', class_="tlmenu")
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
            download_dir=newpath.replace('/','\\')
            payload = {'txtLoginUsername': 'huynguyen104798@gmail.com', 'txtLoginPassword': 'nguyenvanhuy'}
            with requests.Session() as session:
                post = session.post("https://hoc247.net/tai-khoan/dang-nhap.html", data=payload, verify=False)
                req = session.get(link)
            req = req.text
            soup = BeautifulSoup(req,'lxml')
            url = soup.find('a', class_="btn btn-lg btn-download")['href']
            #login
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
            products_data.to_csv(r"")

        #_________cungthi.online_
        elif soup.find('div', class_="center") != None and 'cungthi' in link :
            title_local =soup.find('ul', class_="breadcrumb")
            title_local = title_local.find_all('li', class_="active")
            bigfolder = title_local[1].text
            bigfolder = bigfolder.replace(' ','')
            bigfolder = bigfolder.replace('\n','')
            smallfolder =title_local[2].text
            smallfolder = smallfolder.replace(' ','')
            smallfolder = smallfolder.replace('\n','')
            newpath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\cungthii/' + bigfolder + '/' + smallfolder
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
            products_data.to_csv(r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\cungthi247url\chitiet.csv")

            _, _, files = next(os.walk(r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\Download\cungthii"))
            file_count = len(files)
            print(file_count)


        else:
            products_data.loc[products_data['link'] == link, 'download'] = ''
            products_data.to_csv(
                r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\247url\sinhoc247.csv")

            continue


download()