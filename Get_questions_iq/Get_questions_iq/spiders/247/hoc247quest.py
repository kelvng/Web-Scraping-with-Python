
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
        "SubjectName": "Vật lý",
        "Title": "Lớp 12",
        "ExamName": "Đề thi thử THPT QG 2019 môn Vật lý trường THPT Lý Thái Tổ- Bắc Ninh lần 1",
        "Error": False,
        "Object": {
            "isAlreadyDone": False,
            "details": ""
        },
        "Code": "uuid"
        }
    products_data = pd.read_csv(
        r'E:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tracnghiemnet\tracnghiemneturl\tracngnoeng.csv')

    products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']['link']
    list_link = products_data.loc[products_data['download'] != 'Die']['link'].head(200)
    #50
    link = ['https://hoc247.net/de-thi-thu-thpt-qg-nam-2019-mon-toan-truong-thpt-chuyen-thai-nguyen-lan-1-ktdt4321.html']
    dem =0
    #dem = 40 +150
    base ='https://hoc247.net'
    for link in tqdm(list_link):
        payload = {'txtLoginUsername': 'huynguyen104798@gmail.com', 'txtLoginPassword': 'nguyenvanhuy'}
        with requests.Session() as session:
            post = session.post("https://hoc247.net/tai-khoan/dang-nhap.html", data=payload, verify=False)
            req = session.get(link)
        req = req.text
        soup = BeautifulSoup(req, 'lxml')
        if soup.find('button', class_="btn btn_orange_sm nuthong") == None:
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(
                r"E:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\logadethi.csv")
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
        quest_local = quest_local.find_all('li', class_="lch 336")
        for i in quest_local:
            url = i.find('a')
            url = url['href']
            if 'http' in url:
                url =url
            else:
                url = base + url
            list_url.append(url)

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
                    img_head_ask = requests.get(img_url).content
                    img_name_ask = lecture+ '_'+ " CauSo" + str(g+1) + '.png'
                    filepath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\hoc247img\img_answer/'
                    with open(filepath + img_name_ask, "wb") as im_h:
                        im_h.write(img_head_ask)
                else:
                    content_decode = content_decode
                    pass
            #get ansswer
            answer_local = soup.find('ul',class_="339 dstl")
            answer_lst = answer_local.find_all('li')
            #True_false
            true_text = soup.find('p', class_='fleft w100per martop10')
            true_text = true_text.find('strong').text
            true_text = true_text.split(":")
            true_text = true_text[1]
            true_text =str(true_text).replace(' ','')
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
                            img_head_ans = requests.get(img_ans_url)
                            img_name_ans = lecture+ '_'+  " CauTraLoi" + str(g+1) + '.png'
                            filepath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\hoc247img\img_answer/'
                            with open(filepath + img_name_ans, "wb") as im:
                                im.write(img_head_ans.content)
                            answer_get = j.text
                        else:
                            answer_get = j.text
                            answer = answer
                        if answer_get != '    ':
                            answer_get = j.text
                            answer = answer
                except:
                    pass
                x = j.find_all('span')[0].text
                def checkTF(x):
                    if str(true_text) in x:
                        return True
                    else:
                        return False


                def checkType(answer):
                    if answer.find("img"):
                        return "Text"
                    else:
                        return "Text"

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
                        'Code': 'Image',
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
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        dem += 1
        filename = lecture + '_' + str(dem) + '.json'
        filePath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\247\hoc247json/'
        with open(filePath + filename, "w") as f:
            # with open(filename, "w") as f:
            f.write(data_string)
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(
            r"E:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\logadethi.csv")

    end = datetime.now()
    end_time = end.strftime("%H:%M:%S")
    print(end_time)
get_tracnghiemnet()