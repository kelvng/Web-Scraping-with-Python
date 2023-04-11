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

name = "CoreEduSpider"

list_url = []
datapush = {
    "BotCode": "tailieu123.vn",
    "Url": "LIST URL",
    "TimeScan": "END TIME",
    "FileDownloadJson": [],
    "DownloadFile": "2000",
    "FileResultData": "nơi lưu trữ"
    }
# data json for
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
# with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\jsontestbaitap123\toanhoctest.json',
#         'r') as j:
#     list_link = json.loads(j.read())
products_data = pd.read_csv(
    r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\baitap123url\baitap123.csv')
#list_link = tqdm(products_data['link'].head(200).tolist())
products_data['download'] = np.nan
list_link = products_data.loc[products_data['download'] != 'Yes']['link'].head(5)
list_link = tqdm(list_link)
def get_question():
    demdownload = 0
    dem = 0
    cau = 0

    global title, title_img
    filedownload = []
    for link in list_link:
        # browser.get(link)
        payload = {'dn_user': 'smart-work ', 'dn_pass': 'Langnghiem79'}
        with requests.Session() as session:
            post = session.post("https://www.baitap123.com/thanh-vien/dang-nhap.html", data=payload, verify=False)
            req = session.get(link)
        list_url.append(link)
        page_source = req.text
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            order = soup.find("div", class_="xacnhan_top").text
        except:
            products_data.loc[products_data['link'] == link, 'download'] = 'Fail'
            products_data.to_csv(
                r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\baitap123url\baitap123.csv")
            continue

        time = soup.find('div', class_='xacnhan_bottom').text
        lecture = soup.find('span', class_='money').text  #
        subject = order.split("\n")[1]  # subject

        Title = order.split("\n")[2]  # title
        myUUID = uuid.uuid4()
        str(myUUID)
        data["SubjectName"] = subject
        data["Title"] = Title
        data["Code"] = str(myUUID)
        data["ExamName"] = lecture
        # request
        link_exam = soup.find('a', class_="btn btn-primary")
        link_exam = link_exam['href']
        if 'http' not in link_exam:
            link_exam = 'https://www.baitap123.com' + link_exam
        else:
            link_exam = link_exam
        with requests.Session() as session:
            post = session.post("https://www.baitap123.com/thanh-vien/dang-nhap.html", data=payload, verify=False)
            req = session.get(link_exam)
        page_source = req.text
        dapan_source = BeautifulSoup(page_source, 'html.parser')
        sleep(1)
        list_title = []
        # print(data)
        List_of_source = dapan_source.findAll(True, {'class':
                                                         ['lb_question_item pagi_page_1',
                                                          'lb_question_item pagi_page_2',
                                                          'lb_question_item pagi_page_3',
                                                          'lb_question_item pagi_page_4',
                                                          'lb_question_item pagi_page_5',
                                                          'lb_question_item pagi_page_6']})
        list_filedownload = []
        list_filedownload.clear()
        for i in List_of_source:
            cau += 1
            title_local = i.find('div', class_='lb_cauhoi')
            # contents(là thẻ con của title_local)
            title_decode = ''.join(map(str, title_local.contents))

            # lấy url hình ảnh.
            Lst_img = []
            for p in title_local.find_all('p'):
                if p.find("img"):
                    if 'latex.php' in p.find("img")["src"]:
                        title_img = None
                    else:
                        title_local_img = p.find('img')
                        title_img = title_local_img["src"]
                        Lst_img.append(title_img)
            title_img = '_'.join(Lst_img)
            # download ảnh
            try:
                if title_local.find("img"):
                    img_url = title_local.find("img")["src"]
                    if 'latex.php' in img_url:
                        pass
                    else:
                        img_head_ask = requests.get(img_url)
                        img_name_ask = subject + "-" + lecture + " CauSo" + str(cau) + '.png'
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/image_all/Ask/'
                        with open(filepath + img_name_ask, "wb") as im_h:
                            im_h.write(img_head_ask.content)
                        demdownload += 1
                        list_filedownload.append(img_name_ask)
            except:
                pass

            #
            def checkQuestionmedia():
                if title_local.find('img'):
                    if 'latex.php' in title_local.find('img')['src']:
                        return False
                    else:
                        return True
                else:
                    return False

            # duration
            timeask = time.split("\n")[2]
            timeask = re.findall("\d+", timeask)
            if len(timeask) == 0:
                Time = 10
            else:
                Time = int(timeask[0])
            myUUID = uuid.uuid4()
            str(myUUID)
            list_answer = []

            dict2 = {
                'Id': cau,
                'Order': None,
                'Duration': Time,
                'Unit': 'MINUTE',
                'Mark': 10,
                'Content': title_decode,
                'QuestionMedia': [
                    {
                        'Code': 'VIDEO',
                        'Name': 'Video',
                        'Icon': 'play',
                        'Url': '',
                        'Check': False
                    },
                    {
                        'Code': 'Image',
                        'Name': 'Image',
                        'Icon': 'image',
                        'Url': title_img,
                        'Check': checkQuestionmedia()
                    },
                    {
                        'Code': 'VOICE',
                        'Name': 'Voice',
                        'Icon': 'microphone-alt',
                        'Url': '',
                        'Check': False
                    }
                ],
                'Code': str(myUUID),
                'Type': 'QUIZ_SING_CH',
                'AnswerData': list_answer,
                'IdQuiz': None,
                'UserChoose': None
            }
            list_title.append(dict2)

            answer_loca = i.find_all('div', class_='lb_q_row')
            for s in answer_loca:
                # answer = s.find("span", onclick_= "return lb_choose_dapan(this);")
                answer = s.find('span', class_="lb_q_text")

                if s.find("img"):
                    if 'latex.php' in s.find("img")["src"]:
                        answer_decode = ''.join(map(str, answer.contents))
                        answer_img = None
                    else:
                        answer_decode = ''.join(map(str, answer.contents))
                        answer_get = answer.find("img").attrs["src"]
                        answer_img = answer.find("img").attrs["src"]
                else:
                    answer_decode = ''.join(map(str, answer.contents))
                    answer_text = answer.text
                    answer_get = answer_text.replace("                                 ", "")
                    answer_get = answer_get.replace("\n", "\\n")
                    answer_img = None
                    if answer_get != '    ':  # dont change answer_get != '    '
                        answer_get = answer_get

                # download hinh anh
                try:
                    if answer.find("img"):
                        img_ans_url = answer.find("img")['src']
                        if 'latex.php' in img_ans_url:
                            pass
                        else:
                            img_head_ans = requests.get(img_ans_url)
                            img_name_ans = subject + "-" + lecture + " CauTraLoi" + str(cau) + '.png'
                            filepath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\image_all\Answer/'
                            with open(filepath + img_name_ans, "wb") as im:
                                im.write(img_head_ans.content)
                            demdownload += 1
                            list_filedownload.append(img_name_ans)
                except:
                    pass

                def checkTrueFalse(s):
                    if s.find("img", class_="imgTick"):
                        return True
                    else:
                        return False

                def checkType(s):
                    if s.find("img"):
                        if 'latex.php' in s.find("img")["src"]:
                            return "TEXT"
                        else:
                            return "TEXT"
                    else:
                        return "TEXT"

                myUUID = uuid.uuid4()
                str(myUUID)

                answerdata = {
                    'Code': str(myUUID),
                    'Answer': answer_decode,
                    'Url': answer_img,
                    'Type': "TEXT",
                    'ContentDecode': answer_get,
                    'IsAnswer': None
                }
                list_answer.append(answerdata)
            # print(len(list_answer))
        sleep(2)
        print(len(list_title))
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        data_string = data_string.lstrip()

        def checkstatus():
            if len(list_filedownload) == 0:
                return False
            else:
                return True

        filedownloadjson = {
            "url": link,
            "fileDownloadname": list_filedownload,
            "status": checkstatus()
        }
        filedownload.append(filedownloadjson)
        dem += 1
        # save json
        filename = subject + "-" + lecture + '_' + str(dem) + '.json'
        # filePath = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\json_all/'
        filePath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\json_all/'
        print(filePath + filename)
        with open(filePath + filename, "w") as f:
            f.write(data_string)
        products_data.loc[products_data['link'] == link, 'download'] = 'Yes'
        products_data.to_csv(
            r"C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\baitap123url\baitap123.csv")
        cau = 0
        sleep(1)
    datapush['FileDownloadJson'] = filedownload
    datapush['DownloadFile'] = demdownload


get_question()
#upload data go
endtime = datetime.now()
end_time = endtime.strftime("%H:%M:%S")
print("Current Time =", end_time)
# filePathsave = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Toanhoc'
datapush['TimeScan'] = end_time
datapush['BotCode'] = 'domain'
datapush['Url'] = list_url
filename = name + '_' + 'summary' + '.json'
datapush_obj = json.dumps(datapush, indent=4)
filePath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Toanhoc\summary/'
with open(filePath + filename, 'w') as summary:
    summary.write(datapush_obj)
# check size
size = 0
filePath = r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Toanhoc'
for ele in os.scandir(filePath):
    size += os.stat(ele).st_size
File_Result_Data = {
    'FilePath': filePath,
    'FileSize': size
}
data = {
    'SessionCode': 'domain',
    'StartTime': '',
    'EndTime': end_time,
    'UrlScanJson': list_url,
    'FileDownloadJson': datapush['FileDownloadJson'],
    'NumOfFile': datapush['DownloadFile'],
    'FileResultData': File_Result_Data,
    'NumPasscap': '',
    'UserIdRunning': '001',
    'Ip': '1',
    'Status': 'active',
    'BotCode': "domain",
    'CreatedBy': 'admin',
}
data_obj = json.dumps(data, indent=4)
with open("subjectbaitap123sumanry.json", 'w') as summary:
    summary.write(datapush_obj)

sys.exit()
# C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\json_all/Hóa học 10-Bài số 3 - TH_1693.json
#  15%|█▌        | 648/4249 [2:49:57<15:44:30, 15.74s/it]
