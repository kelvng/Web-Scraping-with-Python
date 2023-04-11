
import json
import os
import re
import sys
import uuid
from datetime import datetime
from time import sleep
from selenium import webdriver
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_tracnghiemnet():
    global list_answer, answer_get
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
        r'D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\questloga.csv')

    #products_data['download'] = np.nan
    list_link = products_data.loc[products_data['download'] != 'Yes']
    list_link = list_link.loc[list_link['download'] != 'Die']['link'].head(50)
    #50
    link = ['https://loga.vn/de-thi/de-thi-thu-toan-chuyen-nguyen-tat-thanh-2019-lan-1-12425']
    dem =0
    #dem = 40 +150
    base ='https://loga.vn'
    for link in tqdm(list_link):
        req = requests.get(link, verify= False)
        page_source = req.text
        soup = BeautifulSoup(page_source,'lxml')
        try:
            subject = soup.find('div', class_='col-md-3 col-xs-6 txt-subject-name').text
            print(subject)
            lecture = soup.find('h1', class_='labExamName').text

        except:
            products_data.loc[products_data['link'] == link, 'download'] = 'Die'
            products_data.to_csv(r'D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\questloga.csv')
            continue
        title = 'Đề thi'
        time = soup.find_all('div', class_="col-md-3 col-xs-6")[1].text
        order = soup.find('div', class_="col-md-3 col-xs-6 txt-question-number").text
        order = order.replace('\n','')
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
        quest_local = soup.find_all('div', class_="div-label-anwser")
        for i in quest_local:
            url = i.find('a')
            url = url['href']
            if 'http' in url:
                url =url
            else:
                url = 'https://loga.vn' + url
            list_url.append(url)
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(
            r"D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\questloga.csv")

#
        list_title = []
        for g in range(len(list_url)):
            link = list_url[g]
            req =requests.get(link, verify=False)
            page_source = req.text
            soup = BeautifulSoup(page_source, 'lxml')
            ask_local = soup.find('div', class_="div-label-anwser")
            #print(ask_local)
            #break hêre
            content_decode =ask_local.find_all('p')
            content_decode = '\n'.join(map(str, content_decode))
            if ask_local.find('img') != None:
                data_src = ask_local.find('img')
                data_src = data_src['src']
                if 'http' not in data_src:
                    newdata_src = base + data_src
                else:
                    newdata_src = data_src
                content_decode = str(content_decode).replace(data_src,newdata_src)
            else:
                content_decode = content_decode
            try:
                if content_decode.find("img"):
                    img_url = content_decode.find("img")["src"]
                    if 'http' not in img_url:
                        img_url = 'https://loga.vn' + img_url
                    else:
                        img_url = img_url
                    img_head_ask = requests.get(img_url).content
                    img_name_ask = lecture+ '_'+ " CauSo" + str(g+1) + '.png'
                    filepath = r'D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaIMG\imageask/'
                    with open(filepath + img_name_ask, "wb") as im_h:
                        im_h.write(img_head_ask)

            except:
                pass
            #get ansswer
            answer_local = soup.find('div',class_="col-sm-12 div-content-anwser")
            answer_lst = answer_local.find_all('div', class_="col-sm-12 div-anwser")
            #True_false
            true_location = soup.find('div', class_="center")
            true_location = true_location.find('div', class_="col-md-6 col-xs-12")
            true_box = true_location.find('button')
            print(true_box)
            if 'ViewAnwser(1)' in str(true_box):
                check = 'labelA'
            elif 'ViewAnwser(2)' in str(true_box):
                check = 'labelB'
            elif 'ViewAnwser(3)' in str(true_box):
                check = 'labelC'
            elif 'ViewAnwser(4)' in str(true_box):
                check = 'labelD'
            #print('true' + str(true_box))
            list_answer=[]
            list_answer.clear()
            for j in answer_lst:
                answer = j.find('label')
                if answer.find('img') != None:
                    data_src = answer.find('img')['src']
                    if 'http' not in data_src:
                        newdata_src = base + data_src
                    else:
                        newdata_src = data_src
                    answer = str(answer).replace(data_src, newdata_src)
                else:
                    answer = j.find('label')


                try:
                    if answer.find("img"):
                        img_ans_url = answer.find("img")['src']
                        if 'http' not in img_ans_url:
                            img_ans_url= 'https://loga.vn' + img_ans_url
                        else:
                            img_ans_url = img_ans_url
                        img_head_ans = requests.get(img_ans_url)
                        img_name_ans = lecture+ '_Huy_'+  " CauTraLoi" + str(g+1) + '.png'
                        filepath = r'D:\PycharmProjects\Source/'
                        #filepath = r'D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tracnghiemnet\image\image_answer/'
                        with open(filepath + img_name_ans, "wb") as im:
                            im.write(img_head_ans.content)
                        answer_get = answer.text + answer.find("img").attrs["src"]
                    else:
                        answer_get = answer.text
                    if answer_get != '    ':
                        answer_get = answer_get
                except :
                    pass
                def checkTF():
                    if str(check) in str(answer):
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
                    'IsAnswer': checkTF()
                }
                print(answerdata)
                list_answer.append(answerdata)
            timeask = time.split("\n")[0]
            timeask = re.findall("\d+", timeask)
            if len(timeask) == 0:
                Time = 10
            else:
                Time = int(timeask[0])
            myUUID = uuid.uuid4()
            str(myUUID)
            options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            options.add_experimental_option("prefs", prefs)
            options.add_argument("start-maximized")
            options.add_argument("user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
            options.add_argument('--headless')
            browser = webdriver.Chrome(r'D:\PycharmProjects\Source\chromedriver.exe', options=options)


            browser.get(link)
            browser.find_element_by_xpath('//*[@class="btn btn-danger width100"]').click()
            sleep(1)
            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            text = soup.find('div', class_="col-sm-12 div-content-anwser")
            x = text.find_all('div')
            solver = x[-4]
            img = solver.find_all('img')
            for i in img:
                img_link = i['src']
                if 'http' in img_link:
                    img_link = img_link
                else:
                    img_link = 'https://loga.vn/' + img_link
                solver = str(solver).replace(i['src'], img_link)
            browser.delete_all_cookies()
            browser.quit()
            # print(solver)
            #print(str(content_decode))
            # if img_name_ask == '':
            #     img_name_ask = ''
            # else:
            #     img_name_ask = img_name_ask
            dict2 = {
                'Id': g+1,
                'Order': order,
                'Duration': Time,
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
                        'Check': False,
                        'MathPixResult':{
                            'text': str(content_decode)
                        }
                    },
                    {
                        'Code': 'VOICE',
                        'Name': 'Voice',
                        'Icon': 'microphone-alt',
                        'Url': '',
                        'Check': False,
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
        filePath = r'D:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\Json/'
        if 'Vật Lý' in subject:
            filePath = filePath + 'Vật Lý' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        if 'Hóa Học' in subject:
            filePath = filePath + 'Hóa Học' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        if 'Toán' in subject:
            filePath = filePath + 'Toán' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        if 'Sinh Học' in subject:
            filePath = filePath + 'Sinh Học' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        if 'Tiếng Anh' in subject:
            filePath = filePath + 'Tiếng Anh' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        if 'Lịch Sử' in subject:
            filePath = filePath + 'Lịch Sử' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        if 'Địa Lý' in subject:
            filePath = filePath + 'Địa Lý' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        if 'GDCD' in subject:
            filePath = filePath + 'GDCD' + '/'
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            pass
        with open(filePath + filename, "w") as f:
            # with open(filename, "w") as f:
            f.write(data_string)

    end = datetime.now()
    end_time = end.strftime("%H:%M:%S")
    print(end_time)
get_tracnghiemnet()
sys.exit()