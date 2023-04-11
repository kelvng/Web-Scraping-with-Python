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



options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Edge(executable_path=r'/msedgedriver.exe',
                         options=options)
name = "quizzz"
def get_quizizz():
    dem =0
    cau =0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\quizz.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
        list_link = json.loads(j.read())
    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
    # for link in tqdm(products_data['link'].tolist()):
        browser.get(link['link'])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        #subject = soup.find("div", class_="text-xxs text-dark-4").text
        try:
            lecture = soup.find("div",class_="quiz-name text-sm font-semibold md:font-regular md:text-xl text-dark-2 my-1 flex items-center").text
            lecture = soup.find("div", class_="quiz-name text-sm font-semibold md:font-regular md:text-xl text-dark-2 my-1 flex items-center").text
        except:
            pass
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
        data["SubjectCode"] = "subject"
        data["Title"] = None
        data["Code"] = None
        data["ID"] = None
        data["LectureCode"] = lecture
        # data["Object"]["details"] = list

        List_of_source = soup.find_all("div", class_="p-4 shadow-md")
        list_title = []
        for i in List_of_source:
            cau += 1

            title_local = i.find("div", class_="flex items-center mb-4")
            try:
                if title_local.find("img"):
                    img_url = title_local.find("img")["src"]
                    img_head_ask = requests.get(img_url)
                    img_name_ask = lecture + " CauSo" + str(cau) + '.png'
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/quizizz/image/'
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
            #time = int(str(time)[:2])
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
            answer_loca = i.find_all("div", class_="mb-2 flex items-start w-1/2")
            for s in answer_loca:

                answer = s.find("span", class_= "text-sm text-dark-2")
                try:
                    if answer.find("img"):
                        img_ans_url = answer.find("img")['src']
                        img_head_ans = requests.get(img_ans_url)
                        img_name_ans = lecture + " CauTraLoi" + str(cau) + '.png'
                        filepath = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\quizizz\image\Img_answer/'
                        with open(filepath + img_name_ans, "wb") as im:
                            im.write(img_head_ans.content)
                except:
                    pass
                #answer_get = answer.text
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
                    # answer_get = answer_get.replace("\n", " ")
                    if answer_get != '    ':
                        answer_get = answer_get
                print(answer_get)

                try:
                    def checkTrueFalse(s):
                        if s.find("span", class_="w-4 h-4 rounded-full my-1 mr-2 relative flex-shrink-0 bg-green"):
                            return True
                        else:
                            return False

                    def checkType(answer):
                        if answer.find("img"):
                            return "Image"
                        else:
                            return "Text"
                except:
                    pass
                myUUID = uuid.uuid4()
                str(myUUID)
                answerdata = {
                    'Code': str(myUUID),
                    'Answer': answer_source,
                    'Type': checkType(answer),
                    'ContentDecode': answer_get,
                    'IsAnswer': checkTrueFalse(s)
                }

                list_answer.append(answerdata)
            print(len(list_answer))
        print(list_title)
        print(len(list_title))
        data["Object"]["details"] = list_title
        # print(data)
        data_string = json.dumps(data, indent=4)
        data_string = data_string.lstrip()
        dem += 1
        lecture = lecture.replace("\n","")
        lecture = lecture.replace("           ","")
        filename = lecture + '_' + str(dem) +'.json'
        filePath = r'/Get_questions_iq/Get_questions_iq/spiders/quizizz/Json/'
        with open(filePath + filename, "w") as f:
            f.write(data_string)

        cau = 0
    browser.quit()
get_quizizz()

sys.exit()