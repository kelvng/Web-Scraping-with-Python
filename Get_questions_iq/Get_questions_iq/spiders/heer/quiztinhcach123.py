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


#khai bao broswer
options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Edge(executable_path=r'/msedgedriver.exe',
                         options=options)

# class baitap123(scrapy.Spider):
#     name = "baitap123"
#     allowed_domains = ['https://www.baitap123.com/']

name = "baitap123"
def login():

    pass

def get_link_source():
    dem = 0
    cau = 0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
    #     list_link = json.loads(j.read())
    # for link in list_link:
    products_data = pd.read_csv(r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/baitap123url/questIQ.csv')
    for link in tqdm(products_data['link'].tolist()):
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        try:
            browser.find_element_by_xpath('//*[@type="radio"]').click()
            sleep(0.5)
            browser.find_element_by_xpath('//*[@type="radio"]').click()
            sleep(0.5)
            browser.find_element_by_xpath('//*[@class="nopbai btn btn-primary btn-lg"]').click()
            sleep(0.5)
            page_source = browser.page_source
            dapan_source = BeautifulSoup(page_source, 'lxml')
        except:
            continue
        # browser.quit()


        time = soup.find("span", class_="lb_count_down hasCountdown").text
        subject = soup.find("h2", class_="h1_monhoc").text
        lecture = soup.find("div", class_="lb_info").text
            # dict1 = {
            #     'ID': 0,
            #     'SubjectCode': subject,
            #     'Title': None,
            #     'LectureCode': lecture,
            #     'Error': False,
            #     'Object': {
            #         'isAlreadyDone': False,
            #         'details': 'list_dict2'
            #     },
            #     "Code": None
            # }
        data["SubjectCode"] = subject
        data["Title"] = None
        data["Code"] = None
        data["ID"] = None
        data["LectureCode"] = lecture
        #data["Object"]["details"] = list
        list_title = []

        List_of_source = dapan_source.find_all("div", class_="lb_question_item pagi_page_1")

        for i in List_of_source:
            cau += 1

            title_local = i.find("div", class_="lb_cauhoi")
            try:
                if title_local.find("img"):
                    img_url = title_local.find("img")["src"]
                    img_head_ask = requests.get(img_url)
                    img_name_ask = lecture + " CauSo" + str(cau) + '.png'
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/image/img_ask/'
                    with open(filepath + img_name_ask, "wb") as im_h:
                        im_h.write(img_head_ask.content)
            except:
                pass
            if  title_local.find("img"):
                title = title_local.text +''+ title_local.find("img").attrs["src"]

            else:
                title = title_local.text
                if title != '\n ':
                    title = title


            time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': 10,
                        'Duration': time,
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
            answer_loca = i.find_all("div", class_= "lb_q_row")
            for s in answer_loca:

                answer = s.find("span", class_= "lb_q_text")
                try:
                    if answer.find("img"):
                        img_ans_url = answer.find("img")['src']
                        img_head_ans = requests.get(img_ans_url)
                        img_name_ans = lecture + " CauTraLoi" + str(cau) + '.png'
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/image/Img_answer/'
                        with open(filepath + img_name_ans, "wb") as im:
                            im.write(img_head_ans.content)
                except:
                    pass
                if answer.find("img"):

                    answer_imgtext = answer.find("img").attrs["alt"]
                    answer_source = answer_imgtext + ' ' + answer_get
                    answer_get = answer.find("img").attrs["src"]

                else:
                    answer_source = answer.text
                    answer_get = answer.text
                    answer_get = answer_get.replace("                                   ", "")
                    answer_get = answer_get.replace("\n", " ")
                    if answer_get != '    ':
                        answer_get = answer_get

                #print(answer_get)

                def checkTrueFalse(s):
                    if s.find("img", class_="imgTick"):
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
                    'IsAnswer': checkTrueFalse(s)
                }

                        #list_answer.append(answerdata)
                list_answer.append(answerdata)

            print(len(list_answer))
        print(list_title)
        print(len(list_title))
        data["Object"]["details"] = list_title
            # print(data)

        data_string = json.dumps(data, indent=4)
        data_string = data_string.lstrip()

        dem += 1
        try:
            filename = lecture + '_' + str(dem) + '.json'

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/QUESTIONIQ/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

get_link_source()
sys.exit()
# for:
#     dict1 = {
#         'ID': 0,
#         'SubjectCode': '',
#         'Title': '',
#         'LectureCode': '',
#         'Error': False,
#         'Object': {
#             'isAlreadyDone': False,
#             'details': 'list_dict2'
#                 },
#         "Code": None
#     }
# # json = json.dumps(dict1, indent=4)
#     list_dict2 = []
#     for:
# #loop title
#         dict2 = {
#             'Id': 1,
#             'Order': 10,
#             'Duration': 10,
#             'Unit': 'MINUTE',
#             'Mark': 10,
#             'Content': '',
#             'QuestionMedia': [
#                             {
#                                 'Code': 'VIDEO',
#                                 'Name': 'Video',
#                                 'Icon': 'play',
#                                 'Url': '',
#                                 'Check': False,
#                                 '$$hashKey': 'object:55'
#                             },
#                             {
#                                 'Code': 'Image',
#                                 'Name': 'Image',
#                                 'Icon': 'image',
#                                 'Url': '',
#                                 'Check': False,
#                                 '$$hashKey': 'object:56'
#                             },
#                             {
#                                 'Code':'VOICE',
#                                 'Name':'Voice',
#                                 'Icon':'microphone-alt',
#                                 'Url':'',
#                                 'Check': False,
#                                 '$$hashKey':'object:57'
#                             }
#                         ],
#             'Code': 'SAMPLE_QUIZ_01',
#             'Type': 'QUIZ_SING_CH',
#             'AnswerData':'',
#             'IdQuiz': 75,
#             'UserChoose': None
#         }
#         for:
#             answerdata = {
#                 'Code': 'str(myUUID)',
#                 'Answer': 'answer_source',
#                 'Type': 'checkType(answer)',
#                 'ContentDecode': 'answer_get',
#                 'IsAnswer': 'checkTrueFalse(s)'
#                 }

