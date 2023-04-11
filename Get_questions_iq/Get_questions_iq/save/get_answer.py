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


content = []

options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Edge(executable_path=r'C:\Users\Admin\PycharmProjects\Source\msedgedriver.exe',
                               options=options)

def get_quizizz():
    with open(r"C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\link.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
        list_link = json.loads(j.read())
    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
    # for link in tqdm(products_data['link'].tolist()):

        browser.get(link['link'])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        # browser.find_element_by_xpath('//*[@type="radio"]').click()
        # browser.find_element_by_xpath('//*[@type="radio"]').click()
        # sleep(0.5)
        # browser.find_element_by_xpath('//*[@class="nopbai btn btn-primary btn-lg"]').click()
        # page_source = browser.page_source
        # dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()

        subject = soup.find("div", class_="text-xxs text-dark-4").text
        lecture = soup.find("div",
                        class_="quiz-name text-sm font-semibold md:font-regular md:text-xl text-dark-2 my-1 flex items-center").text
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
        data["ID"] = 123
        data["LectureCode"] = lecture
        # data["Object"]["details"] = list

        List_of_source = soup.find_all("div", class_="p-4 shadow-md")
        list_title = []
        for i in List_of_source:
            try:
                title_local = i.find("div", class_="flex items-center mb-4")
                if  title_local.find("img"):
                    title = title_local.text +''+ title_local.find("img").attrs["src"]
                else:
                    title = title_local.text
                    if title != '\n ':
                        title = title
            except:
                pass
            list_answer = []
            dict2 = {
                'Id': 1,
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
            answer_loca = i.find_all("div", class_="flex flex-wrap")
            for s in answer_loca:

                answer = s.find("div", class_= "mb-2 flex items-start w-1/2")
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
                    answer_get = answer_get.replace("                                   ", "")
                    answer_get = answer_get.replace("\n", " ")
                    if answer_get != '    ':
                        answer_get = answer_get
                #print(answer_get)

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
        deep = str(1)
        filename = lecture + '_' + deep
        filePath = '\Get_questions_iq/' + filename + '.json'
        with open(filename + ".json", "w") as f:
            f.write(data_string)

def get_hoctainhavn():
    with open(r"C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\baitap123.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)

    with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
        list_link = json.loads(j.read())
    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
    # for link in tqdm(products_data['link'].tolist()):

        browser.get(link['link'])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        id = browser.find_element_by_xpath('//*[@id="txtLoginEmail"]')
        id.send_keys("huynguyen104798@gmail.com")
        pwd = browser.find_element_by_xpath('//*[@id="txtLoginPass"]')
        pwd.send_keys("nguyenvanhuy")
        sleep(1)
        browser.find_element_by_xpath("//*[@value='Đăng nhập']").click()
        sleep(1)
        browser.find_element_by_xpath('//*[@type="radio"]').click()
        # browser.find_element_by_xpath('//*[@type="radio"]').click()
        sleep(0.5)
        browser.find_element_by_xpath('//*[@onclick="return DeThi_Finish();"]').click()
        browser.switch_to.alert.accept()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')
        # # browser.quit()


        # subject = soup.find("div", class_="text-xxs text-dark-4").text
        # lecture = soup.find('h1').get_text()
        lecture = soup.find_all('h1')
        data["SubjectCode"] = None
        data["LectureCode"] = lecture
        data["Title"] = None
        list_title = []
        ContentDecode = []
        #name = dapan_source.find("div", class_= "kq_level").text
        List_of_source = dapan_source.find_all("div", class_="dethi-cauhoi")
        for i in List_of_source:
            title_local = i.find("div", style_="float: left;margin-left:40px;clear:both")
            # if  title_local.find("img"):
            #     title = title_local.text +''+ title_local.find("img").attrs["src"]
            # else:
            title = title_local.text
            if title != '\n ':
                title = title
            list_title.append(title)

            # answer_loca = i.find_all("label", class_= "flex flex-wrap")
            # list_answer = []
            # for s in answer_loca:
            #
            #     answer = s.find("div", class_= "mb-2 flex items-start w-1/2")
            #     if answer.find("img"):
            #         answer_imgtext = answer.find("img").attrs["alt"]
            #         answer_get = answer.find("img").attrs["src"]
            #         answer_source = answer_imgtext + ' ' + answer_get
            #     else:
            #         answer_source = answer.text
            #         answer_get = answer.text
            #         answer_get = answer_get.replace("                                   ", "")
            #         answer_get = answer_get.replace("\n", " ")
            #         if answer_get != '    ':
            #             answer_get = answer_get
            #     #print(answer_get)
            #     def checkTrueFalse(s):
            #         if s.find("span", class_="w-4 h-4 rounded-full my-1 mr-2 relative flex-shrink-0 bg-green"):
            #             return True
            #         else:
            #             return False
            #     def checkType(answer):
            #         if answer.find("img"):
            #             return "Image"
            #         else:
            #             return "Text"
            #     myUUID = uuid.uuid4()
            #     str(myUUID)
            #
            #     answerdata = {
            #         'Code': str(myUUID),
            #         'Answer': answer_source,
            #         'Type': checkType(answer),
            #         'ContentDecode': answer_get,
            #         'IsAnswer': checkTrueFalse(s)
            #     }
            #
            #     list_answer.append(answerdata)
            # ContentDecode.append(list_answer)
        print(list_title)
        print(len(list_title))
        print(ContentDecode)
        print(len(ContentDecode))
        # j = 0
        # while j < len(list_title):
        #     data["Object"]["details"][j]["Content"] = list_title[j]
        #     data["Object"]["details"][j]["AnswerData"] = ContentDecode[j]
        #     data["Object"]["details"][j]["Duration"] = 20
        #     j += 1


        # print(data)
        # data_string = json.dumps(data, indent=4)
        # data_string = data_string.lstrip()
        #
        # # if 'https://' in link['link']:
        # #     filename = link['name'].strip('https://')
        # # if '.vn' in filename:
        # #     filename = filename.strip('.vn')
        # deep = str(1)
        #
        # filename = lecture + '_' + deep
        #
        # filePath = '\Get_questions_iq/' + filename + '.json'
        # with open(filename + ".json", "w") as f:
        #     f.write(data_string)

def get_vuihocvn():
    with open(r"C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\baitap123.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)

    with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
        list_link = json.loads(j.read())
    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
    # for link in tqdm(products_data['link'].tolist()):

        browser.get(link['link'])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        # lecture = soup.find('div', class_="banner-title").text
        try:
            browser.find_element_by_xpath('//*[@title="Đăng nhập"]').click()
            id = browser.find_element_by_xpath('//*[@id="loginFormEmail"]')
            id.send_keys("0394544777")
            pwd = browser.find_element_by_xpath('//*[@id="loginFormPassword"]')
            pwd.send_keys("anhhuyc3")
                # sleep(1)
            browser.find_element_by_xpath("//*[@class='loginBtn']").click()
            sleep(1)
        except:
            pass

        browser.find_element_by_xpath('//*[@class="no-choice-answer init-a"]').click()
        sleep(0.5)
        browser.find_element_by_xpath('//*[@class="no-choice-answer init-a"]').click()
        # browser.find_element_by_xpath('//*[@type="radio"]').click()
        sleep(0.5)
        browser.find_element_by_xpath('//*[@class="nopbai"]').click()
        sleep(0.5)
        # browser.switch_to.alert.accept()
        browser.find_element_by_xpath('//*[@class="confirm btn btn-lg btn-success"]')
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        subject = soup.find("div", class_="text-xxs text-dark-4").text
        lecture = soup.find("div",class_="quiz-name text-sm font-semibold md:font-regular md:text-xl text-dark-2 my-1 flex items-center").text

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
        data["ID"] = 123
        data["LectureCode"] = lecture
        # data["Object"]["details"] = list

        List_of_source = soup.find_all("div", class_="course-item")
        list_title = []

        for i in List_of_source:
            try:
                title_local = i.find("div", class_="text")
                # if  title_local.find("img"):
                #     title = title_local.text +''+ title_local.find("img").attrs["src"]
                # else:
                title = title_local.text
                if title != '\n ':
                    title = title
            except:
                pass
            list_answer = []
            dict2 = {
                'Id': 1,
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
            answer_loca = i.find_all("div", class_="btn-group")

            for s in answer_loca:

                answer = s.find("label", class_= "label-btn-group")
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
                #print(answer_get)
                try:
                    def checkTrueFalse(answer):
                        if answer.find("span", class_="no-choice-answer init-a init-correct-answer"):
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
        print(list_title)
        print(len(list_title))
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        data_string = data_string.lstrip()
        deep = str(1)
        filename = lecture + '_' + deep
        filePath = '\Get_questions_iq/' + filename + '.json'
        with open(filename + ".json", "w") as f:
            f.write(data_string)

def get_hocmaivn():
    with open(r"C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\baitap123.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
        list_link = json.loads(j.read())
    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
    # for link in tqdm(products_data['link'].tolist()):

        browser.get(link['link'])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@type="radio"]').click()
        browser.find_element_by_xpath('//*[@type="radio"]').click()
        sleep(0.5)
        browser.find_element_by_xpath('//*[@class="nopbai btn btn-primary btn-lg"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')
        # browser.quit()


        subject = soup.find("div", class_="text-xxs text-dark-4").text
        lecture = soup.find("div", class_="quiz-name text-sm font-semibold md:font-regular md:text-xl text-dark-2 my-1 flex items-center").text
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
        data["ID"] = 123
        data["LectureCode"] = lecture
        # data["Object"]["details"] = list

        List_of_source = soup.find_all("div", class_="p-4 shadow-md")
        list_title = []
        for i in List_of_source:
            try:
                title_local = i.find("div", class_="flex items-center mb-4")
                if  title_local.find("img"):
                    title = title_local.text +''+ title_local.find("img").attrs["src"]
                else:
                    title = title_local.text
                    if title != '\n ':
                        title = title
            except:
                pass
            list_answer = []
            dict2 = {
                'Id': 1,
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
            answer_loca = i.find_all("div", class_= "flex flex-wrap")
            for s in answer_loca:

                answer = s.find("div", class_= "mb-2 flex items-start w-1/2")
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
                    answer_get = answer_get.replace("                                   ", "")
                    answer_get = answer_get.replace("\n", " ")
                    if answer_get != '    ':
                        answer_get = answer_get
                #print(answer_get)
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
                    myUUID = uuid.uuid4()
                    str(myUUID)
                except:
                    pass
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
        deep = str(1)
        filename = lecture + '_' + deep
        filePath = '\Get_questions_iq/' + filename + '.json'
        with open(filename + ".json", "w") as f:
            f.write(data_string)

def get_tuyensinh47():
    with open(r"C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\baitap123.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
        list_link = json.loads(j.read())
    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
    # for link in tqdm(products_data['link'].tolist()):

        browser.get(link['link'])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@type="radio"]').click()
        browser.find_element_by_xpath('//*[@type="radio"]').click()
        sleep(0.5)
        browser.find_element_by_xpath('//*[@class="nopbai btn btn-primary btn-lg"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')
        # browser.quit()


        subject = soup.find("div", class_="text-xxs text-dark-4").text
        lecture = soup.find("div", class_="quiz-name text-sm font-semibold md:font-regular md:text-xl text-dark-2 my-1 flex items-center").text
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
        data["ID"] = 123
        data["LectureCode"] = lecture
        # data["Object"]["details"] = list

        List_of_source = soup.find_all("div", class_="p-4 shadow-md")
        list_title = []
        for i in List_of_source:
            try:
                title_local = i.find("div", class_="flex items-center mb-4")
                if  title_local.find("img"):
                    title = title_local.text +''+ title_local.find("img").attrs["src"]
                else:
                    title = title_local.text
                    if title != '\n ':
                        title = title
            except:
                pass
            list_answer = []
            dict2 = {
                'Id': 1,
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
            answer_loca = i.find_all("div", class_= "flex flex-wrap")
            for s in answer_loca:

                answer = s.find("div", class_= "mb-2 flex items-start w-1/2")
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
                    answer_get = answer_get.replace("                                   ", "")
                    answer_get = answer_get.replace("\n", " ")
                    if answer_get != '    ':
                        answer_get = answer_get
                #print(answer_get)
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
                    myUUID = uuid.uuid4()
                    str(myUUID)
                except:
                    pass
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
        deep = str(1)
        filename = lecture + '_' + deep
        filePath = '\Get_questions_iq/' + filename + '.json'
        with open(filename + ".json", "w") as f:
            f.write(data_string)

