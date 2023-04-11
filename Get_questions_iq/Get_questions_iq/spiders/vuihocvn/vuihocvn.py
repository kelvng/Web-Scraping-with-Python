import sys
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

name = "vuihoc"
def login():
    browser.get("https://vuihoc.vn/")
    wait = WebDriverWait(browser, 1)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnLogin"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginFormEmail"]'))).send_keys("0394544777")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginFormPassword"]'))).send_keys("anhhuyc3")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="loginBtn"]'))).click()
    sleep(1)


def get_vuihocvn():
    global dapan_source
    dem =0
    cau = 0
    login()
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)

    with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\vuihocvn.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
        list_link = json.loads(j.read())

    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
    # for link in tqdm(products_data['link'].tolist()):
        browser.get(link["link"])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        lecture = soup.find("div", class_="banner-title").text
        data["SubjectCode"] = None
        data["Title"] = None
        data["Code"] = None
        data["ID"] = 123
        data["LectureCode"] = lecture
        # data["Object"]["details"] = list
        sleep(1)
        browser.find_element_by_xpath('//*[@class="example"]').click()
        browser.switch_to.window(browser.window_handles[1])
        page_source = browser.page_source
        Soup = BeautifulSoup(page_source, 'lxml')
        try:
            if Soup.find('div', class_="result text-red"):
                dapan_source = Soup
            else:
                browser.find_element_by_xpath('//*[@class="no-choice-answer init-a"]').click()
                sleep(0.5)
                browser.find_element_by_xpath('//*[@class="nopbai"]').click()
                sleep(0.5)
                browser.find_element_by_xpath('//*[@class="sa-confirm-button-container"]').click()
                sleep(1)
                page_source = browser.page_source
                dapan_source = BeautifulSoup(page_source, 'lxml')

        except:
            pass
        List_of_source = dapan_source.find_all("div", class_="course-item")
        list_title = []
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        try:
            for i in List_of_source:
                cau += 1
                title_local = i.find("div", class_="text")
                try:
                    if title_local.find("img"):
                        img_url = title_local.find("img")["src"]
                        img_head_ask = requests.get(img_url)
                        img_name_ask = lecture + " CauSo" + str(cau) + '.png'
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/vuihocvn/image/'
                        with open(filepath + img_name_ask, "wb") as im_h:
                            im_h.write(img_head_ask.content)
                except:
                    continue
                try:

                    if title_local.find("img"):
                        title = title_local.text + '' + title_local.find("img").attrs["src"]
                    else:
                        title = title_local.text
                    if title != '\n ':
                        title = title
                except:
                    pass
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
                answer_loca = i.find_all("label", class_="label-btn-group")

                for s in answer_loca:
                    answer = s.find("span", class_="content-answer")
                    try:
                        if answer.find("img"):
                            img_ans_url = answer.find("img")['src']
                            img_head_ans = requests.get(img_ans_url)
                            img_name_ans = lecture + " CauTraLoi" + str(cau) + '.png'
                            filepath = r'/Get_questions_iq/Get_questions_iq/spiders/vuihocvn/image/'
                            with open(filepath + img_name_ans, "wb") as im:
                                im.write(img_head_ans.content)
                    except:
                        continue
                    answer = s.find("span", class_="content-answer")
                    if answer.find("img"):
                        try:
                            answer_imgtext = answer.find("img").attrs["alt"]
                            answer_get = answer.find("img").attrs["src"]
                            answer_source = answer_imgtext + ' ' + answer_get
                        except:
                            pass
                    else:
                        answer_source = answer.text
                        answer_get = answer.text
                        # answer_get = answer_get.replace("                                   ", "")
                        answer_get = answer_get.replace("\n", " ")
                        if answer_get != '    ':
                            answer_get = answer_get
                    # print(answer_get)
                    try:
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
                    except:
                        pass

                    answerdata = {
                        'Code': str(myUUID),
                        'Answer': answer_source,
                        'Type': checkType(answer),
                        'ContentDecode': answer_get,
                        'IsAnswer': checkTrueFalse(answer)
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
        filePath = r'/Get_questions_iq/Get_questions_iq/spiders/vuihocvn/json/'
        print(filePath + filename)
        with open(filePath + filename, "w") as f:
            f.write(data_string)
        cau = 0
    browser.quit()

get_vuihocvn()
sys.exit()