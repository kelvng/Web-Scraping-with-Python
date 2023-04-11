
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
    # products_data = pd.read_csv(
    #     r'D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tracnghiemnet\tracnghiemneturl\tienganh.csv')
    #
    # #products_data['download'] = np.nan
    # list_link = products_data.loc[products_data['download'] != 'Yes']
    # list_link = list_link.loc[list_link['download'] == 'Die']
    # list_link = list_link.loc[list_link['download'] != 'checkagain']['link']
    #50
    link = ['https://tracnghiem.net/de-thi/de-thi-hk1-mon-tieng-anh-12-nam-2021-2022-4109.html','https://tracnghiem.net/thptqg/de-thi-thu-thpt-qg-nam-2022-mon-tieng-anh-5454.html']
    dem =0
    #dem = 40 +150
    for link in link:
        req = requests.get(link, verify= False)
        sleep(1)
        page_source = req.text
        soup = BeautifulSoup(page_source,'lxml')
        try:
            soup.find('div', class_="card-header")
            infor = soup.find('div', class_="detail-question")
            order = infor.find("div", class_="num-question col").text
        except:
            # products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            # products_data.to_csv(
            #     r"D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tracnghiemnet\tracnghiemneturl\tracngnoeng.csv")
            continue
        examcontent = soup.find('div', class_='exam-content')
        lecture = soup.find('h1').text
        if lecture == '':
            text = link
            text = text.replace('https://tracnghiem.net/', '')
            text = text.replace('-', ' ')
            head, sep, tail = text.partition('.html')
            head, sep, tail = head.partition('/')
            lecture = tail
        print(lecture)


        order = re.findall(r'\d+', str(order))
        order = int(order[0])
        time = infor.find("div", class_="num-minutes col")

        if time == None:
            time = None
        else:
            time = time.find('span').text
            time = re.findall(r'\d+', str(time))
            time = int(time[0])

        subjet = soup.find('ol', class_="breadcrumb")
        sub = subjet.find_all('a')
        subject = sub[2].text
        print(subject)
        title = sub[1].text
        myUUID = uuid.uuid4()
        str(myUUID)
        data["SubjectName"] = subject
        data["Title"] = title
        data["Code"] = str(myUUID)
        data["ID"] = None
        data["ExamName"] = lecture
        try:
            lstlink = examcontent.find_all('a')
        except:
            pass
        # link of a box  styple of quest.
        list_url = []
        list_ask = []

        for i in lstlink:
            #break
            url = i['href']
            if 'https://tracnghiem' in url:
                list_url.append(url)
                ask_decode = i.find_all('p')
                ask_decode = '\n'.join(map(str, ask_decode))
                list_ask.append(ask_decode)
            else:
                pass

        list_title = []
        if len(list_url) == len(list_ask):
            print( "TRUE WAY NICE GUY!")
        for g in range(len(list_url)):
            link = list_url[g]
            content_decode = list_ask[g]
            req =requests.get(link, verify=False)
            page_source = req.text

            soup = BeautifulSoup(page_source, 'lxml')
            numb_of_ask = soup.find_all('div', class_="part-item detail question-detail")
            for ask in numb_of_ask:
                box_ask = ask.find('div', class_="d9Box part-item detail question-detail")
                text = box_ask.find('p').text
                answer_local = box_ask.find_all('div', class_='radio-control')
                try:
                    if content_decode.find("img"):
                        img_url = content_decode.find("img")["src"]
                        img_head_ask = requests.get(img_url).content
                        img_name_ask = lecture+ '_'+ text + " CauSo" + str(g+1) + '.png'
                        filepath = r'D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tracnghiemnet\image\image_ask/'
                        with open(filepath + img_name_ask, "wb") as im_h:
                            im_h.write(img_head_ask)

                except:
                    pass
                true_box = soup.find('div', class_="question-result")
                true_box = true_box.find('div', class_="result-row wrong-result")
                true_box = true_box.find('span', class_="right-answer")
                text_true = true_box.find('b').text + '.'

                list_answer = []
                for j in answer_local:
                    answer = j.find('label', class_="custom-control-label")
                    try:
                        if answer.find("img"):
                            img_ans_url = answer.find("img")['src']
                            img_head_ans = requests.get(img_ans_url)
                            img_name_ans = lecture+ '_'+ text + " CauTraLoi" + str(g+1) + '.png'
                            filepath = r'D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tracnghiemnet\image\image_answer/'
                            with open(filepath + img_name_ans, "wb") as im:
                                im.write(img_head_ans.content)
                            answer_get = answer.text + answer.find("img").attrs["src"]
                        else:
                            answer_get = answer.text
                        if answer_get != '    ':
                            answer_get = answer_get
                    except:
                        pass

                    def checkTF(j):
                        if text_true in answer_get:
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
                        'Answer': str(answer),
                        'Type': checkType(answer),
                        'ContentDecode': answer_get,
                        'IsAnswer': checkTF(j)
                    }
                    list_answer.append(answerdata)

                myUUID = uuid.uuid4()
                str(myUUID)
                solver = soup.find('div',class_="answer-result")
                dict2 = {
                    'Id': g+1,
                    'Order': order,
                    'Duration': time,
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

        print(len(list_title))
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        dem += 1
        filename = lecture + '_' + str(dem) + '.json'
        #filename = 'Huy' + '.json'
        filePath = r'Json/'
        if 'Tiếng Anh' in subject:
            filePath = r'E:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tracnghiemnet\Json2/' + 'Tiếng Anh' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass

        print(filename)
        with open(filePath + filename, "w") as f:
            # with open(filename, "w") as f:
            f.write(data_string)

    end = datetime.now()
    end_time = end.strftime("%H:%M:%S")
    print(end_time)
get_tracnghiemnet()
sys.exit()