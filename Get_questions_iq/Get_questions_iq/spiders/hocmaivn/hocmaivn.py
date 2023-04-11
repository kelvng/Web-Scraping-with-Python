from datetime import datetime
import json
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

options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Edge(executable_path=r'/msedgedriver.exe',
                         options=options)

name = "hocmaivn"


def login():
    browser.get("https://hocmai.vn/")
    wait = WebDriverWait(browser, 1)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn-acc btn-login"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys("huynguyen104798@gmail.com")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys("stop-pillo")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="submit register-btn"]'))).click()
    sleep(1)


def get_hocmaivn():

    dem = 0
    cau = 0
    login()
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r',
              encoding="utf8") as outfile:
        data = json.load(outfile)

    with open(r'/Get_questions_iq/Get_questions_iq/spiders/JSon/hocmaitest.json',
              'r') as j:
        # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
        list_link = json.loads(j.read())

    for link in list_link:
        # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
        # for link in tqdm(products_data['link'].tolist()):
        browser.get(link["link"])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        lecture = soup.find("div", class_="pr-a-title").text
        # Time = soup.find('span', id_="minutes").text
        Title = lecture.split("\n")[1] #
        sleep(2)
        dapan_source = soup

        data["SubjectCode"] = None
        data["Title"] = Title
        data["Code"] = None
        data["ID"] = 123
        data["LectureCode"] = lecture
        # data["Object"]["details"] = list
        List_of_source = dapan_source.find("div", class_="box_quiz_content")
        List_of_source = List_of_source.find_all("div", class_="content")
        list_title = []
        try:
            for i in List_of_source:
                cau += 1
                title_local = i.find("div", class_="qtext")
                try:
                    if title_local.find("img"):
                        img_url = title_local.find("img")["src"]
                        img_head_ask = requests.get(img_url)
                        img_name_ask = lecture + " CauSo" + str(cau) + '.png'
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/hocmaivn/Image/img_ask/'
                        with open(filepath + img_name_ask, "wb") as im_h:
                            im_h.write(img_head_ask.content)
                except:
                    continue

                if title_local.find("img"):
                    title = title_local.text + '' + title_local.find("img").attrs["src"]
                else:
                    title = title_local.text
                    if title != '\n ':
                        title = title
                list_answer = []
                dict2 = {
                    'Id': cau,
                    'Order': 10,
                    'Duration': "Time",
                    'Unit': 'MINUTE',
                    'Mark': 10,
                    'Content': title,
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
                    'Code': 'SAMPLE_QUIZ_01',
                    'Type': 'QUIZ_SING_CH',
                    'AnswerData': list_answer,
                    'IdQuiz': 75,
                    'UserChoose': None
                }
                list_title.append(dict2)
                answer_loca = i.findAll(True, {'class': ['r0','r1']})
                #print(answer_loca)

                for s in answer_loca:
                    answer = s.find("td", class_="c1 text")
                    try:
                        if answer.find("img"):
                            img_ans_url = answer.find("img")['src']
                            img_head_ans = requests.get(img_ans_url)
                            img_name_ans = lecture + " CauTraLoi" + str(cau) + '.png'
                            filepath = r'/Get_questions_iq/Get_questions_iq/spiders/hocmaivn/Image/image_answer/'
                            with open(filepath + img_name_ans, "wb") as im:
                                im.write(img_head_ans.content)
                    except:
                        continue
                    if answer.find("img"):
                        answer_imgtext = answer.find("img").attrs["alt"]
                        answer_get = answer.find("img").attrs["src"]
                        answer_source = answer_imgtext + ' ' + answer_get
                    else:
                        answer_source = answer.text
                        answer_get = answer.text
                        # answer_get = answer_get.replace("                                   ", "")
                        answer_get = answer_get.replace("\n", " ")
                        if answer_get != '    ':
                            answer_get = answer_get
                    # print(answer_get)

                    def checkTrueFalse(s):
                        if s.find("span", class_="no-choice-answer init-a init-correct-answer"):
                            return True
                        else:
                            return False

                    def checkType(answer):
                        if answer.find("img"):
                            return "Image"
                        else:
                            return "Text"

                    myUUID = uuid.uuid4()
                    str(myUUID)


                    answerdata = {
                        'Code': str(myUUID),
                        'Answer': answer_source,
                        'Type': checkType(answer),
                        'ContentDecode': answer_get,
                        'IsAnswer': None
                    }

                    list_answer.append(answerdata)
                print(len(list_answer))
        except:
            pass
        print(list_title)
        print(len(list_title))
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        data_string = data_string.lstrip()
        dem += 1
        lecture = lecture.replace("\n", "")
        lecture = lecture.replace("           ", "")
        filename = lecture + '_' + str(dem) + '.json'
        filePath = r'/Get_questions_iq/Get_questions_iq/spiders/hocmaivn/Json/'
        print(filePath + filename)
        with open(filePath + filename, "w") as f:
            f.write(data_string)
        cau = 0
    browser.quit()


get_hocmaivn()
