import csv
import json
import os
import re
from datetime import datetime
#VIP.
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

# login

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}

options.add_experimental_option("prefs", prefs)
options.add_argument("--start-maximized")
options.add_argument("log-level=3")
# options.add_argument('--headless')
browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
browser.get('https://suretest.vn/')
sleep(1)
browser.find_element_by_xpath('//*[@id="menu-login"]').click()
sleep(1)
#login
mail = browser.find_element_by_xpath('//*[@id="UserName"]')
mail.send_keys('zetabase3i@gmail.com')
password = browser.find_element_by_xpath('//*[@id="Password"]')
password.send_keys('Langnghiem79')
browser.find_element_by_xpath('//*[@onclick="SignIn()"]').click()

sleep(2)

def get_tracnghiemnet():
    #login()
    data = {
        "ID": 0,
        "SubjectName": "Sinh học 12",
        "Title": "Liên kết gen và hoán vị gen ",
        "ExamName": "Bài số 2 - TH",
        "Error": False,
        "Object": {
            "isAlreadyDone": False,
            "details": ""
        },
        "Code": "uuid"
        }
    #
    # products_data = pd.read_csv(
    #     r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\url\url.csv')
    #
    # products_data['download'] = np.nan
    # list_link = products_data.loc[products_data['download'] != 'Yes']['link'].head(5)
    #50
    link_test = ['https://suretest.vn/luyen-thi/de-thi-toan-thpt-quoc-gia-nam-2018-%E2%80%93-ma-de-114-bo-giao-duc-va-dao-tao-1505.html','https://suretest.vn/luyen-thi/de-thi-toan-thpt-quoc-gia-nam-2018-–-ma-de-115-bo-giao-duc-va-dao-tao-1506.html']
    dem =1
    #dem = 40 +150

    for link in tqdm(link_test):
        print(link)
        try:

            browser.get(link)
        except:
            browser.get(link)
        sleep(2)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source,'lxml')

        if soup.find('div', class_="col-xs-12 col-sm-4 text-center div-info-l") != None:
            Lst_data = soup.find('ol', class_="breadcrumb")
            Lst_data = Lst_data.find_all('li')
            Subject_Name = Lst_data[2].text
            Title_Name = Lst_data[1].text
            title = soup.find_all('h2', class_="section-title hidden-xs text-center text-uppercase")
            lecture = title[0].text
            myUUID = uuid.uuid4()
            str(myUUID)
            data["SubjectName"] = Subject_Name
            data["Title"] = Title_Name
            data["Code"] = str(myUUID)
            data["ExamName"] = lecture
            pass
        else:
            Lst_data = soup.find('ol', class_="breadcrumb")
            print(Lst_data)
            Lst_data = Lst_data.find_all('li')
            Subject_Name = Lst_data[2].text
            Title_Name = Lst_data[1].text
            title = soup.find('h2', class_="text-info")
            lecture = title.text
            myUUID = uuid.uuid4()

            str(myUUID)
            data["SubjectName"] = Subject_Name
            data["Title"] = Title_Name
            data["Code"] = str(myUUID)
            data["ExamName"] = lecture

            try:
                browser.find_element_by_xpath('//*[@class="btn btn-primary input-lg"]').click()
                sleep(2)
                browser.find_element_by_xpath('//*[@type="radio"]').click()
                check_quest = browser.find_element_by_xpath('//*[@id="SubmitTask"]')
                check_quest.click()
                sleep(0.5)
                browser.find_element_by_xpath('//*[@class="icon-submit-custom fa fa-file-text"').click()
                sleep(0.5)
                browser.find_elements_by_xpath('//*[@class="btn btn-success btn-gogo key-enter"]')[1].click()

            except:
                print("ko phải câu hỏi")
                # products_data.loc[products_data['link'] == link, 'download'] = 'Die'
                # products_data.to_csv(
                #     r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\url\url.csv")

                continue
            pass

        print(Subject_Name)
        print(Title_Name)
        print(lecture)

        page_source = browser.page_source
        soup1= BeautifulSoup(page_source,'lxml')
        Lst_Content = []
        local_ask = soup1.find_all('div', class_="section-cnt")
        for value in local_ask:
            content = value.contents
            ask_content = ' '.join(map(str, content))
            Lst_Content.append(ask_content)

        lst_answer = soup1.find_all('div', class_="ques ques-actived")
        if len(local_ask) == len(lst_answer):
            print('Yes')
            pass
        else:
            print('CheckAgain')
            continue
        list_title = []
        for j in range(len(lst_answer)):
            Content = Lst_Content[j]
            Lst_content = lst_answer[j].find_all('li')
            list_answer = []
            try:
                Solve = lst_answer[j].find('div', class_="col-xs-12 col-md-12 col-lg-11").contents
                Solve_content = ' '.join(map(str, Solve))
            except:
                pass
            for h in Lst_content:
                answer = h.find('div', class_="div-content")
                answer_content = ' '.join(map(str,answer))
                if 'class="result"' in answer_content:
                    TF = True
                else:
                    TF = False
                sleep(0.15)
                myUUID = uuid.uuid4()
                str(myUUID)
                answerdata = {
                    'Code': str(myUUID),
                    'Answer': str(answer_content),
                    'Type': 'TEXT',
                    'ContentDecode': str(answer_content),
                    'IsAnswer': TF
                }
                list_answer.append(answerdata)
            myUUID = uuid.uuid4()
            str(myUUID)
            dict2 = {
                'Id': j,
                'Order': 20,
                'Duration': 20,
                'Unit': 'MINUTE',
                'Mark': 10,
                'Content': str(Content),
                'Solve': {
                    'Solver': str(Solve_content),
                    'SolveMedia': [
                        {
                            'Code': 'VIDEO',
                            'Name': 'Video',
                            'Icon': 'play',
                            'Url': '',
                            'Check': False
                        },
                        {
                            'Code': 'IMAGE',
                            'Name': 'Image',
                            'Icon': 'image',
                            'Url': '',
                            'Check': False
                        },
                        {
                            'Code': 'VOICE',
                            'Name': 'Voice',
                            'Icon': 'microphone-alt',
                            'Url': '',
                            'Check': False
                        }
                    ]
                },
                'QuestionMedia': [
                    {
                        'Code': 'VIDEO',
                        'Name': 'Video',
                        'Icon': 'play',
                        'Url': '',
                        'Check': False,
                        '$$hashKey': 'object:55'
                    },
                    {
                        'Code': 'IMAGE',
                        'Name': 'Image',
                        'Icon': 'image',
                        'Url': '',
                        'Check': False,
                        '$$hashKey': 'object:56'
                    },
                    {
                        'Code': 'VOICE',
                        'Name': 'Voice',
                        'Icon': 'microphone-alt',
                        'Url': '',
                        'Check': False,
                        '$$hashKey': 'object:57'
                    }
                ],
                'Code': str(myUUID),
                'Type': 'QUIZ_SING_CH',
                'AnswerData': list_answer,
                'IdQuiz': None,
                'UserChoose': None
            }
            list_title.append(dict2)
        print(len(list_title))
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        print(data_string)
        dem += 1
        filename = lecture
        filename = filename.replace(':', "")
        filename = filename.replace('/', "")
        filename = filename.replace('\\', "")
        filename = filename.replace('*', "")
        filename = filename.replace('|', "")
        filename = filename.replace('\n', "")
        filename = filename.replace('?', "") + '_' + str(dem) + '.json'
        filePath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\suretest\Json/'
        print(filename)
        with open(filePath + filename, "w") as f:
            f.write(data_string)
        # products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        # products_data.to_csv(
        #     r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\url\tech12htracnghiem.csv")
        list_title.clear()

        end = datetime.now()
        end_time = end.strftime("%H:%M:%S")
        print(end_time)




get_tracnghiemnet()
