import csv
import json
import os
import re
from datetime import datetime

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
    products_data = pd.read_csv(
        r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\url\tech12htracnghiem.csv')

    products_data['download'] = np.nan
    products_data = products_data.loc[products_data['download'] != 'NOTQUEST']
    list_link = products_data.loc[products_data['download'] != 'CheckAgain']['link'].head(10)
    #50
    link_test = ['https://tech12h.com/bai-hoc/trac-nghiem-cong-dan-11-bai-3-quy-luat-gia-tri-trong-san-xuat-va-luu-thong-hang-hoa-p1.html','https://tech12h.com/bai-hoc/trac-nghiem-cong-dan-11-bai-6-cong-nghiep-hoa-hien-dai-hoa-dat-nuoc-p1.html','https://tech12h.com/bai-hoc/trac-nghiem-cong-dan-11-bai-9-nha-nuoc-xa-hoi-chu-nghia-p1.html']
    dem =1
    #dem = 40 +150

    for link in tqdm(list_link):
        # login

        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}

        options.add_experimental_option("prefs", prefs)
        options.add_argument("--start-maximized")
        options.add_argument("log-level=3")
        # options.add_argument('--headless')
        browser = webdriver.Chrome(r'F:\PycharmProjects\Source\chromedriver.exe', options=options)
        browser.get(link)

        try:
            check_quest = browser.find_element_by_xpath('//*[@class="kqua"]')
            if check_quest!= None:
                pass
            else:
                print("ko phai cau hoi")
                products_data.loc[products_data['link'] == link, 'download'] = 'NOTQUEST'
                products_data.to_csv(
                    r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\url\tech12htracnghiem.csv")

                browser.close()
                browser.quit()
                continue
        except:
            print("ko phải câu hỏi")
            products_data.loc[products_data['link'] == link, 'download'] = 'CheckAgain'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\url\tech12htracnghiem.csv")

            browser.close()
            browser.quit()
            continue

        page_source = browser.page_source
        soup = BeautifulSoup(page_source,'lxml')

        Lst_data= soup.find_all('li', class_="breadcrumb-item")
        Subject_Name = Lst_data[1].text
        Title_Name = Lst_data[2].text
        title = soup.find_all('h1', class_="title-primary title-type-4")
        lecture = title[0].text
        myUUID = uuid.uuid4()
        str(myUUID)
        data["SubjectName"] = Subject_Name
        data["Title"] = Title_Name
        data["Code"] = str(myUUID)
        data["ExamName"] = lecture
        local_quest = soup.find('div', class_="accordion accordion-detail tex2jax")
        Lst_localquest = local_quest.find_all('p')
        LST_QUEST = []
        for j in range(len(Lst_localquest)):
            content = str(Lst_localquest[j])
            if 'Câu' in content:
                LST_QUEST.append(content)
        Lst_localanswer = local_quest.find_all('ul')
        if len(Lst_localanswer) == len(LST_QUEST):
            print("alive")
            pass
        else:
            print('die')
            products_data.loc[products_data['link'] == link, 'download'] = 'CheckAgain'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\url\tech12htracnghiem.csv")

            browser.close()
            browser.quit()
            continue
        list_title = []

        for i in range(len(Lst_localanswer)):
            CONTENT = LST_QUEST[i]
            print(CONTENT)
            lstans = Lst_localanswer[i].find_all('li')
            list_answer = []
            for g in range(len(lstans)):
                answer = str(lstans[g])

                if '</h6>' in answer:
                    TF = True
                else:
                    TF = False
                sleep(0.15)
                myUUID = uuid.uuid4()
                str(myUUID)
                answerdata = {
                    'Code': str(myUUID),
                    'Answer': str(answer),
                    'Type': 'TEXT',
                    'ContentDecode': str(answer),
                    'IsAnswer': TF
                }
                list_answer.append(answerdata)
            myUUID = uuid.uuid4()
            str(myUUID)
            dict2 = {
                'Id': i,
                'Order': 20,
                'Duration': 20,
                'Unit': 'MINUTE',
                'Mark': 10,
                'Content': str(CONTENT),
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
        filename = lecture + '_' + str(dem) + '.json'
        filename = filename.replace(':',"")
        filename = filename.replace('/', "")
        filename = filename.replace('\\', "")
        filename = filename.replace('*', "")
        filename = filename.replace('|', "")
        filename = filename.replace('?', "")
        filePath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\Json/'
        print(filename)
        with open(filePath + filename, "w") as f:
            f.write(data_string)
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(
            r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\Tech12h\url\tech12htracnghiem.csv")
        list_title.clear()
        browser.close()
        browser.quit()
    end = datetime.now()
    end_time = end.strftime("%H:%M:%S")
    print(end_time)




get_tracnghiemnet()
