# coding=utf8
# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import uuid

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_tracnghiemnet():
    #login()

    data = {
        "ID": 0,
        "SubjectName": "",
        "Title": "",
        "ExamName": "",
        "Source": "",
        "Error": False,
        "Object": {
            "isAlreadyDone": False,
            "details": ""
        },
        "Code": "uuid"
        }
    products_data = pd.read_csv(
        r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\congchu24h\Linkurl\de_thi.csv')
    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(500)
    #link = ['https://congchuc24h.com/de-thi-trac-nghiem-thue-mon-kien-thuc-chung-co-dap-an-so-221/']

    dem = 0
    for link in tqdm(list_link):
        print(link)
        req = requests.get(link, verify= False)
        page_source = req.text
        time.sleep(1)
        soup = BeautifulSoup(page_source,'lxml')

        lecture = soup.find('h1', class_="entry-title").text

        lecture = lecture.replace('				','')
        lecture = lecture.replace('\n', '')
        lecture = lecture.replace('\t\t\t','')
        subject = 'Công Chức'
        print(lecture)
        filePath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\congchu24h\Json/'
        if 'kien-thuc-chung' in link:
            title = 'Kiến thức chung'
            filePath = filePath + title + '/'
        elif 'tieng-anh' in link:
            title = 'Ngoại ngữ'
            filePath = filePath + title + '/'
        elif 'tin-hoc' in link:
            title = 'Tin học'
            filePath = filePath + title + '/'
        elif 'trac-nghiem-thue' in link:
            title = 'Thuế'
            filePath = filePath + title + '/'
        elif 'vien-kiem-sat' in link:
            title = 'Viện kiểm sát'
            filePath = filePath + title + '/'
        elif 'thi-hanh-an-dan-su' in link:
            title = 'Thi hành án dân sự'
            filePath = filePath + title + '/'
        elif 'hai-quan' in link:
            title = 'Hải quan'
            filePath = filePath + title + '/'
        elif 'dang-doan-the' in link:
            title = 'Đảng Đoàn Thể'
            filePath = filePath + title + '/'
        elif 'kiem-toan-nha-nuoc' in link:
            title = 'Kiểm Toán nhà nước'
            filePath = filePath + title + '/'
        elif 'y-te' in link:
            title = 'Y tế'
            filePath = filePath + title + '/'
        elif 'giao-vien' in link:
            title = 'Giáo Viên'
            filePath = filePath + title + '/'
        elif 'cong-chuc-xa' in link:
            title = 'Công chức xã'
            filePath = filePath + title + '/'
        elif 'ngan-hang' in link:
            title = 'Ngân Hàng'
            filePath = filePath + title + '/'
        elif 'kho-bac' in link:
            title = 'Kho Bạc'
            filePath = filePath + title + '/'
        elif 'quan-ly-thi-truong' in link:
            title = 'Quản lý thị trường'
            filePath = filePath + title + '/'
        elif 'toa-an' in link:
            title = 'Toà Án'
            filePath = filePath + title + '/'
        elif 'ke-toan' in link:
            title = 'Kế Toán'
            filePath = filePath + title + '/'
        elif 'trac-nghiem-boi-duong' in link:
            title = 'Bồi dưỡng quản lý nhà nước'
            filePath = filePath + title + '/'
        else:
            title = 'Kiến thức chung'
            filePath = filePath + title + '/'
        print(title)
        myUUID = uuid.uuid4()
        data["SubjectName"] = subject
        data["Title"] = title
        data["Code"] = str(myUUID)
        data["ID"] = None
        data["ExamName"] = lecture
        quest = soup.find('div', class_="entry-content clearfix")
        local =  quest.find_all('p')
        print(quest.find_all('div', class_="wp-block-image"))
        if len(quest.find_all('div', class_="wp-block-image")) != 0:
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\congchu24h\Linkurl\de_thi.csv")
            continue
        else:
            pass
        for x in range(len(local)):
            if 'value="B"' in str(local[x]):
                local = str(local[x])
        local = BeautifulSoup(local, 'lxml')

        numb_ask = len(local.find_all('b'))
        #list câu hỏi
        ask_list = local.find_all('b')
        text_true = local.find_all('input')

        lst_true = []
        # get list true ansswer
        for value in text_true:
            if  'visibility: hidden' in str(value):
                lst_true.append(value)
        # lấy list tất cả các câu trả lời
        lst_answer = local.find_all('label')
        list_title = []
        for i in range(numb_ask):
            title_decode = ask_list[i]
            right_answer = str(lst_true[i])
            list_answer= []

            list_answer.clear()
            for value in lst_answer:
                if "choice" + str(i+1) + "A" in str(value):
                    A = str(value)
                    A_decode = value.text
                    def TrueFale():
                        if "A" in right_answer:
                            return True
                        else:
                            return False

                    myUUID = uuid.uuid4()
                    data1 = {
                        "Code":str(myUUID),
                        "Answer":  A,
                        "Type": "TEXT",
                        "ContentDecode": A_decode,
                        "IsAnswer": TrueFale()
                    }
                    list_answer.append(data1)
                if "choice" + str(i+1) + "B" in str(value):
                    B = str(value)
                    B_decode = value.text
                    def TrueFale():
                        if "B" in right_answer:
                            return True
                        else:
                            return False

                    myUUID = uuid.uuid4()
                    data2 = {
                        "Code": str(myUUID),
                        "Answer":  B,
                        "Type": "TEXT",
                        "ContentDecode": B_decode,
                        "IsAnswer": TrueFale()
                    }
                    list_answer.append(data2)
                if "choice" + str(i+1) + "C" in str(value):
                    C = str(value)
                    C_decode = value.text
                    def TrueFale():
                        if "C" in right_answer:
                            return True
                        else:
                            return False

                    myUUID = uuid.uuid4()
                    data3 = {
                        "Code": str(myUUID),
                        "Answer":  C,
                        "Type": "TEXT",
                        "ContentDecode": C_decode,
                        "IsAnswer": TrueFale()
                    }
                    list_answer.append(data3)
                if "choice" + str(i+1) + "D" in str(value):
                    D = str(value)
                    D_decode = value.text
                    def TrueFale():
                        if "D" in right_answer:
                            return True
                        else:
                            return False

                    myUUID = uuid.uuid4()
                    data4 = {
                        "Code": str(myUUID),
                        "Answer":  D,
                        "Type": "TEXT",
                        "ContentDecode": D_decode,
                        "IsAnswer": TrueFale()
                    }
                    list_answer.append(data4)
            myUUID = uuid.uuid4()
            str(myUUID)
            dict2 = {
                'Id': i + 1,
                'Order': None,
                'Duration': None,
                'Unit': 'MINUTE',
                'Mark': 10,
                'Content': str(title_decode),
                'Solve': {
                    'Solver': '',
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
                'IdQuiz': 75,
                'UserChoose': None
            }
            list_title.append(dict2)
        print(list_title)
        print(len(list_title))
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        dem += 1
        filename = lecture + '_' + str(dem) + '.json'
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        print(filePath + filename)
        with open(filePath + filename, "w") as f:
            # with open(filename, "w") as f:
            f.write(data_string)
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(
            r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\congchu24h\Linkurl\de_thi.csv")


get_tracnghiemnet()
sys.exit()