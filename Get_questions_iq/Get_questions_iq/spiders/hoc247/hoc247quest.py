import os
import sys
from datetime import datetime

import numpy as np
from selenium.common.exceptions import NoSuchElementException
import json
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import uuid
from tqdm import tqdm
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

time = datetime.now()
current_time = time.strftime("%H:%M:%S")
print("Current Time =", current_time)

def get_tracnghiemnet():
    global list_answer, answer_get
    #login()
    data = {
        "ID": 0,
        "SubjectName": "",
        "Title": "",
        "ExamName": "",
        "Error": False,
        "Object": {
            "isAlreadyDone": False,
            "details": ""
        },
        "Code": "uuid"
        }
    products_data = pd.read_csv(
        r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\hoc247url\hoc247tracnghiem1.csv')

    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'check']
    list_link = list_link.loc[list_link['download'] != 'Die']['link']
    #50
    link = ['https://hoc247.net/de-thi-thu-thpt-qg-nam-2019-mon-toan-truong-thpt-chuyen-thai-nguyen-lan-1-ktdt4321.html']
    dem =0
    #dem = 40 +150
    base ='https://hoc247.net'
    for link1 in tqdm(list_link):
        print(link1)
        payload = {'txtLoginUsername': 'huynguyen104798@gmail.com', 'txtLoginPassword': 'nguyenvanhuy'}
        with requests.Session() as session:
            post = session.post("https://hoc247.net/tai-khoan/dang-nhap.html", data=payload, verify=False)
            req = session.get(link1)
        req = req.text
        soup = BeautifulSoup(req, 'lxml')
        if soup.find('button', class_="btn btn_orange_sm posrelative0 nuthong") != None:
            products_data.loc[products_data['link'] == link1, 'download'] = 'Check'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\hoc247url\hoc247tracnghiem1.csv")
        else:
            pass
        print(soup.find('button', class_="btn btn_orange_sm nuthong"))
        if soup.find('button', class_="btn btn_orange_sm nuthong") == None  :
            products_data.loc[products_data['link'] == link1, 'download'] = 'Die'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\hoc247url\hoc247tracnghiem1.csv")
            continue
        else:
            pass
        lecture = soup.find('h1', class_="cate-h1").text
        #info
        lesson_info = soup.find('div', class_="lesstion_info")
        time = lesson_info.find('i', class_="fa fa-clock-o").text
        timeask = time.split("\n")[0]
        timeask = re.findall("\d+", timeask)
        if len(timeask) == 0:
            Time = 10
        else:
            Time = int(timeask[0])
        order = lesson_info.find('i', class_="fa fa-question-circle").text
        order = order.split(" ")[0]
        order =str(order)
        local = soup.find('div', class_="breadcrum")
        lst_info= local.find_all('a')
        subject = lst_info[3].text
        title = lst_info[2].text
        myUUID = uuid.uuid4()
        str(myUUID)
        data["SubjectName"] = subject
        data["Title"] = title
        data["Code"] = str(myUUID)
        data["ID"] = None
        data["ExamName"] = lecture

        list_url = []
        list_ask = []
        #find link cuar caau hoir
        quest_local = soup.find('ul', class_='dsch')
        try:

            quest_local = quest_local.find_all('li', class_="lch 336")

            for i in quest_local:
                url = i.find('a')
                url = url['href']
                if 'http' in url:
                    url =url
                else:
                    url = base + url
                list_url.append(url)
        except:
            products_data.loc[products_data['link'] == link1, 'download'] = 'Die'
            products_data.to_csv(
                r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\hoc247url\hoc247tracnghiem1.csv")
            continue

        list_title = []
        for g in range(len(list_url)):
            link = list_url[g]
            payload = {'txtLoginUsername': 'huynguyen104798@gmail.com', 'txtLoginPassword': 'nguyenvanhuy'}
            with requests.Session() as session:
                post = session.post("https://hoc247.net/tai-khoan/dang-nhap.html", data=payload, verify=False)
                req = session.get(link)
            req = req.text
            soup = BeautifulSoup(req, 'lxml')
            ask_local = soup.find('li', class_="lch")
            contentdecode_local =ask_local.find_all('p')
            check = soup.find('div', class_="_traloi displaynone")
            check = check.find_all('p')
            content_decode_lst = contentdecode_local[:len(contentdecode_local) - len(check)]
            content_decode = '\n'.join(map(str, content_decode_lst))

            for i in content_decode_lst:
                if i.find("img"):
                    img_url = i.find("img")["src"]
                    data_src = ask_local.find('img')
                    data_src = data_src['src']
                    if 'http' not in data_src:
                        newdata_src = base + data_src
                    else:
                        newdata_src = data_src
                    content_decode = str(content_decode).replace(data_src, newdata_src)
                    if 'http' not in img_url:
                        img_url = base + img_url
                    else:
                        img_url = img_url
                    try:
                        img_head_ask = requests.get(img_url).content
                        img_name_ask = lecture+ '_'+ " CauSo" + str(g+1) + '.png'
                        filepath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\image\img_ans/'
                        with open(filepath + img_name_ask, "wb") as im_h:
                            im_h.write(img_head_ask)
                    except:
                        pass
                else:
                    content_decode = content_decode
                    pass
            try:
                #get ansswer
                answer_local = soup.find('ul',class_="339 dstl")
                answer_lst = answer_local.find_all('li')
                #True_false
                true_text = soup.find('p', class_='fleft w100per martop10')
                true_text = true_text.find('strong').text
                true_text = true_text.split(":")
                true_text = true_text[1]
                true_text =str(true_text).replace(' ','')
                print(true_text)
                list_answer=[]
                list_answer.clear()
                for j in answer_lst:
                    answer = j.find_all('span')
                    answer = '\n'.join(map(str, answer))
                    try:
                        for h in j.find_all('span'):
                            if h.find("img"):
                                img_ans_url = h.find("img")['src']
                                data_src = h.find('img')['src']
                                if 'http' not in data_src:
                                    newdata_src = base + data_src
                                else:
                                    newdata_src = data_src
                                answer = str(answer).replace(data_src, newdata_src)
                                if 'http' not in img_ans_url:
                                    img_ans_url= base + img_ans_url
                                else:
                                    img_ans_url = img_ans_url
                                try:
                                    img_head_ans = requests.get(img_ans_url)
                                    img_name_ans = lecture+ '_'+  " CauTraLoi" + str(g+1) + '.png'
                                    filepath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\image\img_ask/'
                                    with open(filepath + img_name_ans, "wb") as im:
                                        im.write(img_head_ans.content)
                                    answer_get = j.text
                                except:
                                    pass
                            else:
                                answer_get = j.text
                                answer = answer
                            if answer_get != '    ':
                                answer_get = j.text
                                answer = answer
                    except:
                        pass
                    print(j)
                    try:
                        x = j.find_all('span')[0].text
                        def checkTF(x):
                            if str(true_text) in x:
                                return True
                            else:
                                return False
                    except:
                        pass


                    def checkType(answer):
                        if answer.find("img"):
                            return "TEXT"
                        else:
                            return "TEXT"

                    sleep(0.15)
                    myUUID = uuid.uuid4()
                    str(myUUID)
                    answerdata = {
                        'Code': str(myUUID),
                        'Answer': str(answer),
                        'Type': checkType(answer),
                        'ContentDecode': answer_get,
                        'IsAnswer': checkTF(x)
                    }
                    list_answer.append(answerdata)

                myUUID = uuid.uuid4()
                str(myUUID)

                dict2 = {
                    'Id': g+1,
                    'Order': order,
                    'Duration': Time,
                    'Unit': 'MINUTE',
                    'Mark': 10,
                    'Content': str(content_decode),
                    'Solve': {
                        'Solver': 'Solve Quest',
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
                                'Url': 'title_img',
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
            except:
                pass
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        dem += 1
        filename = lecture + '_' + str(dem) + '.json'

        if 'Lớp 6' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Lớp 6'
        elif 'Lớp 7' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Lớp 7'
        elif 'Lớp 8' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Lớp 8'
        elif 'Lớp 9' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Lớp 9'
        elif 'Lớp 10' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Lớp 10'
        elif 'Lớp 11' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Lớp 11'
        elif 'Lớp 12' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Lớp 12'
        elif 'Đại học' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Đại học'
        elif 'Tiểu Học' in title:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json\Đại học'
        else:
            newpath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\Json'
        subfolder = subject

        filepath = newpath + '\\'+subfolder
        isExist = os.path.exists(filepath)

        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(filepath)
            print("The new directory is created!")

        with open(filepath +'/'+ filename, "w") as f:
            # with open(filename, "w") as f:
            f.write(data_string)
        products_data.loc[products_data['link'] == link1, 'download'] = 'Yes'
        products_data.to_csv(
            r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\hoc247\hoc247url\hoc247tracnghiem1.csv")
    end = datetime.now()
    end_time = end.strftime("%H:%M:%S")
    print(end_time)
get_tracnghiemnet()