import shutil
import sys
from datetime import datetime
import json
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import uuid
from tqdm import tqdm
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import scrapy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import asyncio
import websockets

time =datetime.now()
current_time = time.strftime("%H:%M:%S")
print("Current Time =", current_time)

#khai bao broswer
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
options.add_argument('headless')
browser = webdriver.Chrome(executable_path=r'F:\PycharmProjects\Source\chromedriver.exe',
                               options=options)


with open(r"F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\new.json", 'r',
          encoding="utf8") as outfile:
    data = json.load(outfile)
with open(r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\summary.json', 'r', encoding='utf8') as push:
    datapush = json.load(push)
# with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
#     list_link = json.loads(j.read())
products_data = pd.read_csv(
    r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\baitap123url\questIQ.csv')
list_link = tqdm(products_data['link'].tolist())


domain ="baitap123.com"
name = "IQbaitap123"
list_url = []
def login():
    browser.get('https://www.baitap123.com/')
    wait = WebDriverWait(browser, 1)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("smart-work ")
    # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("Langnghiem79")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
    browser.find_element_by_xpath('//*[@id="fb-closebox"]').click()
    sleep(1)

def get_link_source():
    demdownload = 0
    dem = 0
    cau = 0
    filedownload = []
    for link in list_link:
        #browser.get(link['link'])
        browser.get(link)
        list_url.append(link)
        # list_url.append(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        try:
            browser.find_element_by_xpath('//*[@type="radio"]').click()
            sleep(1.5)
            browser.find_element_by_xpath('//*[@type="radio"]').click()
            sleep(1)
            browser.find_element_by_xpath('//*[@type="radio"]').click()
            browser.find_element_by_xpath('//*[@class="nopbai btn btn-primary btn-lg"]').click()
            sleep(2)
            page_source = browser.page_source
            dapan_source = BeautifulSoup(page_source, 'lxml')
            sleep(3)
        except:
            continue

        subject = soup.find("h2", class_="h1_monhoc").text
        lecture = soup.find("div", class_="lb_info").text

        myUUID = uuid.uuid4()
        str(myUUID)
        data["SubjectName"] = subject
        data["Title"] = None
        data["ID"] = None
        data["ExamName"] = lecture
        data["Code"] = str(myUUID)
        # data["Object"]["details"] = list
        list_title = []

        List_of_source = dapan_source.findAll(True, {
            'class': ['lb_question_item pagi_page_1', 'lb_question_item pagi_page_2', 'lb_question_item pagi_page_3',
                      'lb_question_item pagi_page_4', 'lb_question_item pagi_page_5', 'lb_question_item pagi_page_6']})

        list_filedownload = []
        list_filedownload.clear()
        sleep(2)
        try:
            for i in List_of_source:
                cau += 1
                title_local = i.find("div", class_="lb_cauhoi")

                if  title_local.find("img"):
                    title_decode = ''.join(map(str, title_local.contents))
                    title_img = title_local.find("img").attrs["src"]
                else:
                    title_decode = ''.join(map(str, title_local.contents))
                    title_img = None
                #download img
                try:
                    if title_local.find("img"):
                        img_url = title_local.find("img")["src"]
                        response = requests.get(img_url, stream=True)
                        print(response.raw)
                        img_name_ask = img_url.replace('http://www.baitap123.com/editor/fileman/Uploads/trac_nghiem_vui/TestIQ/','')
                        filepath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\QUESTIONIQ\image\Img_answer/'
                        with open(filepath + img_name_ask, "wb") as im_h:
                            shutil.copyfileobj(response.raw, im_h)
                        demdownload += 1
                        list_filedownload.append(img_name_ask)
                except:
                    pass

                def checkTrueFalse(title_local):
                    if title_local.find("img") and title_local.find('p').text:
                        return False
                    elif title_local.find('p').text:
                        return False
                    else:
                        return True
                list_answer = []
                myUUID = uuid.uuid4()
                str(myUUID)
                dict2 = {
                    'Id': None,
                    'Order': cau,
                    'Duration': 10,
                    'Unit': 'MINUTE',
                    'Mark': 10,
                    'Content': title_decode.replace('http://www.baitap123.com/editor/fileman/Uploads/trac_nghiem_vui/TestIQ/','https://dieuhanh.vatco.vn//uploads/repository/SUBJECT/'),
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
                            'Check': False
                        },
                        {
                            'Code': 'IMAGE',
                            'Name': 'Image',
                            'Icon': 'image',
                            'Url': title_img,
                            'Check': checkTrueFalse(title_local)
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
                answer_loca = i.find_all("div", class_= "lb_q_row")
                for s in answer_loca:
                    answer = s.find("span", class_= "lb_q_text")

                    if answer.find("img"):
                        answer_decode = ''.join(map(str, answer.contents))
                        answer_get = answer.find("img").attrs["src"]
                        answer_img = answer_get
                    else:
                        answer_decode = ''.join(map(str, answer.contents))
                        answer_get = answer.text
                        answer_get = answer_get.replace("                                               ", "")
                        answer_get = answer_get.replace("\n", " ")
                        answer_img = None
                        if answer_get != '    ': # không thay đổi đc
                            answer_get = answer_get
                    #download img
                    try:
                        if answer.find("img"):
                            img_ans_url = answer.find("img")['src']
                            response = requests.get(img_ans_url, stream=True)
                            print(response.raw)
                            img_name_ans = img_ans_url.replace('http://www.baitap123.com/editor/fileman/Uploads/trac_nghiem_vui/TestIQ/','')
                            filepath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\QUESTIONIQ\image\img_ask/'
                            with open(filepath + img_name_ans, "wb") as im:
                                shutil.copyfileobj(response.raw, im)
                            demdownload += 1
                            list_filedownload.append(img_name_ans)
                    except:
                        pass
                    def checkTrueFalse(s):
                        if s.find("img", class_="imgTick"):
                            return True
                        else:
                            return False

                    def checkType(answer):
                        if answer.find("img"):
                            return "IMAGE"
                        else:
                            return "TEXT"
                    sleep(0.15)
                    myUUID = uuid.uuid4()
                    str(myUUID)
                    answerdata = {
                        'Code': str(myUUID),
                        'Answer': answer_decode.replace('http://www.baitap123.com/editor/fileman/Uploads/trac_nghiem_vui/TestIQ/','https://dieuhanh.vatco.vn//uploads/repository/SUBJECT/'),
                        'Url': answer_img,
                        'Type': checkType(answer),
                        'ContentDecode': answer_get.replace('http://www.baitap123.com/editor/fileman/Uploads/trac_nghiem_vui/TestIQ/','https://dieuhanh.vatco.vn//uploads/repository/SUBJECT/'),
                        'IsAnswer': checkTrueFalse(s)
                    }
                    list_answer.append(answerdata)

                # print(len(list_answer))
        except:
            pass

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
        filename = lecture + '_' + str(dem) + '.json'
        filePath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\QUESTIONIQ/'
        print(filePath + filename)
        with open(filePath + filename, "w") as f:
        #with open(filename, "w") as f:
            f.write(data_string)
        cau = 0

    datapush['FileDownloadJson'] = filedownload
    datapush['DownloadFile'] = demdownload
    print(dem)
    browser.quit()
get_link_source()
endtime = datetime.now()
end_time = endtime.strftime("%H:%M:%S")
print("Current Time =", end_time)
    #filePathsave = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Toanhoc'
datapush['TimeScan'] = end_time
datapush['BotCode'] = domain
datapush['Url'] = list_url
filename = name + '_' + 'summary' + '.json'
datapush_obj = json.dumps(datapush, indent=4)
filePath =r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\QUESTIONIQ\summary/'
with open(filePath + filename, 'w') as summary:
    summary.write(datapush_obj)

size = 0

filePath = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\QUESTIONIQ'
for ele in os.scandir(filePath):
    size += os.stat(ele).st_size
print(size)
File_Result_Data = {
    'FilePath':filePath,
    'FileSize':size
}

data = {
                            'SessionCode':domain,
                            'StartTime':'',
                            'EndTime': end_time,
                            'UrlScanJson':list_url,
                            'FileDownloadJson':datapush['FileDownloadJson'],
                            'NumOfFile':datapush['DownloadFile'],
                            'FileResultData':File_Result_Data,
                            'NumPasscap':'',
                            'UserIdRunning':'001',
                            'Ip':'1',
                            'Status':'active',
                            'BotCode':domain,
                            'CreatedBy': 'admin',
}
data_obj = json.dumps(data, indent=4)
with open("../heer/IQbaitap123sumanry.json", 'w') as summary:
    summary.write(datapush_obj)
#add vào sumanry json
print(data)

sys.exit()

#168