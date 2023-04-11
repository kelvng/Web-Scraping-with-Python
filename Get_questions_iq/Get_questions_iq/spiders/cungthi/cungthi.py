
import json
import os
import re
import sys
import uuid
from datetime import datetime
from time import sleep

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_tracnghiemnet():
    global list_answer
    #login()
    data = {
        "ID": 0,
        "SubjectName": "Sinh học 12",
        "Title": "",
        "ExamName": "",
        "Source" : "",
        "Error": False,
        "Object": {
            "isAlreadyDone": False,
            "details": ""
        },
        "Code": "uuid"
        }
    products_data = pd.read_csv(
        r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\cungthi247url\cungthi247quest.csv')

    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']
    list_link = list_link.loc[list_link['download'] != 'checkagain']['link']
    # #50
    link = ['https://cungthi.online/de-thi/toan-hoc/bai-tap-trac-nghiem-15-phut-phuong-trinh-mat-phang-trong-khong-gian-toan-hoc-12-de-so-5-GFQ7255.html']
    dem =0
    #dem = 40 +150
    for link in tqdm(list_link):
        req = requests.get(link, verify= False)
        sleep(1)
        page_source = req.text
        soup = BeautifulSoup(page_source,'lxml')
        try:

            soup = soup.find('div', class_="post-content")
            lecture = soup.find('h1',class_="h1_rewrite").text
        except:
            products_data.loc[products_data['link'] == link, 'download'] = 'DIE'
            products_data.to_csv(
                r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\cungthi247url\cungthi247quest.csv')

            continue
        infor = soup.find('div', class_="post-meta")
        infor =  infor.find_all('a')
        subject = infor[-1].text


        myUUID = uuid.uuid4()
        str(myUUID)
        data["SubjectName"] = ""
        data["Title"] = ""
        data["Code"] = str(myUUID)
        data["ID"] = None
        data["ExamName"] = ""
        #examcontent = soup.find("div", id_='testInstructions')
        lstlink = soup.find_all('div', class_="Container")

        list_url = []
        list_ask = []
        #tag
        for i in lstlink:
            i = i.find('a')
            url = i['href']
            if 'https://cungthi.online' in url:
                list_url.append(url)
                ask_local = i.find('span',class_="ContainerIndent").contents

                ask_decode = '\n'.join(map(str, ask_local))
                list_ask.append(ask_decode)
            else:
                pass

        list_title = []
        if len(list_url) == len(list_ask):
            print( "TRUE WAY NICE GUY!")
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(
            r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\cungthi247url\cungthi247quest.csv')
        for g in range(len(list_url)):
            link = list_url[g]
            content_decode = list_ask[g]
            req =requests.get(link, verify=False)
            page_source = req.text
            soup = BeautifulSoup(page_source, 'lxml')
            questlocal = soup.find('div',class_="post-content")
                # true

            solver_place = questlocal.find_all('div', class_="Container100")[1]
            solver3 = solver_place.find_all('p')
            solver = ''.join(map(str,solver3))
            # truefalse
            texttrue = solver_place.text

            x = texttrue.split("Lời giải:", 1)
            y = x[0].split("Đáp án:", 1)
            True_answer = y[1].replace("\n","").replace(".","")
            print(True_answer)
            answer_local = questlocal.find_all('div',class_="ContainerIndent answer_content")
            list_answer = []
            for j in answer_local:
                #answer = j.find('div', class_="ContainerIndent answer_content")

                checkanswer = j.find('span',class_="answer_unselected").text.replace(".","")
                print(checkanswer)
                answer_decode = j.find_all('span')
                answer_decode = ' '.join(map(str,answer_decode))

                def checkTF(checkanswer):
                    if checkanswer in True_answer :
                        return True
                    else:
                        return False

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
                    'Answer': str(answer_decode),
                    'Type': "TEXT",
                    'ContentDecode': answer_decode,
                    'IsAnswer':  checkTF(checkanswer)
                }
                list_answer.append(answerdata)

            myUUID = uuid.uuid4()
            str(myUUID)
            dict2 = {
                'Id': g+1,
                'Order': 30,
                'Duration': 30,
                'Unit': 'MINUTE',
                'Mark': 10,
                'Content': str(content_decode),
                'Solve': {
                    'Solver': str(solver),
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
                        'Check': False,
                        'MathPixResult':{
                            'text': str(content_decode)
                        }
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

        print(filename)

        if 'toan-hoc' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\Toán/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        elif 'khoa-hoc-xa-hoi' in link:
            path  = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\KHXH/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        elif 'tieng-anh' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\Tiếng anh/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        elif 'vat-ly' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\Vật lý/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        elif 'dia-ly' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\Địa lý/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        elif 'lich-su' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\Lịch sử/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        elif 'sinh-hoc' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\sinh hoc/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        elif 'hoa-hoc' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\Hóa học/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        elif 'khoa-hoc-tu-nhien' in link:
            path = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json\KHTN/'
            if 'lop-1-' in link:
                filePath = path + 'lớp 1' + '/'
            elif 'lop-2-' in link:
                filePath = path + 'lớp 2' + '/'
            elif 'lop-3-' in link:
                filePath = path + 'lớp 3' + '/'
            elif 'lop-4-' in link:
                filePath = path + 'lớp 4' + '/'
            elif 'lop-5-' in link:
                filePath = path + 'lớp 5' + '/'
            elif 'lop-6-' in link:
                filePath = path + 'lớp 6' + '/'
            elif 'lop-7-' in link:
                filePath = path + 'lớp 7' + '/'
            elif 'lop-8-' in link:
                filePath = path + 'lớp 8' + '/'
            elif 'lop-9-' in link:
                filePath = path + 'lớp 9' + '/'
            elif 'lop-10' in link or '-10-' in link:
                filePath = path + 'lớp 10' + '/'
            elif 'lop-11' in link or '-11-' in link:
                filePath = path + 'lớp 11' + '/'
            elif 'lop-12' in link or '-12-' in link:
                filePath = path + 'lớp 12' + '/'
            else:
                filePath = path
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        else:
            filePath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\Json/'
        print(filePath)
        with open(filePath + filename, "w") as f:

            f.write(data_string)
        # products_data.loc[products_data['link'] == link, 'download'] = 'Yes  '
        # products_data.to_csv(
        #     r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\cungthi\cungthi247url\cungthi247quest.csv")


get_tracnghiemnet()
sys.exit()