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
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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
    browser.get('https://www.baitap123.com/')
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    wait = WebDriverWait(browser, 2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
    sleep(2)

def get_hoahoc():
    dem = 0
    cau = 0
    browser.get('https://www.baitap123.com/')
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    wait = WebDriverWait(browser, 2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
    sleep(1)
    try:
        browser.find_element_by_xpath('//*[@id="fb-closebox"]').click()
    except:
        pass
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    with open(r'/Get_questions_iq/Get_questions_iq/spiders/JSon/questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
         list_link = json.loads(j.read())
    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\baitap123url\tracnghiemall.csv')
    # for link in tqdm(products_data['link'].tolist()):

        browser.get(link["link"])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        try:
            browser.find_element_by_link_text("Làm bài trắc nghiệm").click()
        except:
            continue
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()
        try:
            order = soup.find("div", string_="Số câu hỏi: ").text
            time = soup.find("div", string_="Thời gian làm bài: " ).text
            subject = soup.find("h1", class_="h1_monhoc").text
            Title = soup.find("h2", class_="h2_monhoc").text
            lecture = soup.find("span", class_="money").text
            Code = soup.find("div", class_="col_navi").text
        except:
            continue
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Hoahoc/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Hoahoc/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Hoahoc/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

def get_dialy():
    dem = 0
    cau = 0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
    #     list_link = json.loads(j.read())
    # for link in list_link:
    products_data = pd.read_csv(r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/baitap123url/dialy.csv')
    for link in tqdm(products_data['link'].tolist()):
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
        sleep(1)
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@onclick="delete_cookie_lambai();"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()

        order = soup.find("div", string_="Số câu hỏi: ").text
        time = soup.find("div", string_="Thời gian làm bài: " ).text
        subject = soup.find("h1", class_="h1_monhoc").text
        Title = soup.find("h2", class_="h2_monhoc").text
        lecture = soup.find("span", class_="money").text
        Code = soup.find("div", class_="col_navi").text
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Dialy/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Dialy/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Dialy/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

def get_lichsu():
    dem = 0
    cau = 0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
    #     list_link = json.loads(j.read())
    # for link in list_link:
    products_data = pd.read_csv(r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/baitap123url/lichsu.csv')
    for link in tqdm(products_data['link'].tolist()):
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
        sleep(1)
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@onclick="delete_cookie_lambai();"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()

        order = soup.find("div", string_="Số câu hỏi: ").text
        time = soup.find("div", string_="Thời gian làm bài: " ).text
        subject = soup.find("h1", class_="h1_monhoc").text
        Title = soup.find("h2", class_="h2_monhoc").text
        lecture = soup.find("span", class_="money").text
        Code = soup.find("div", class_="col_navi").text
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Lichsu/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Lichsu/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Lichsu/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

def get_nguvan():
    dem = 0
    cau = 0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
    #     list_link = json.loads(j.read())
    # for link in list_link:
    products_data = pd.read_csv(r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/baitap123url/nguvan.csv')
    for link in tqdm(products_data['link'].tolist()):
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
        sleep(1)
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@onclick="delete_cookie_lambai();"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()

        order = soup.find("div", string_="Số câu hỏi: ").text
        time = soup.find("div", string_="Thời gian làm bài: " ).text
        subject = soup.find("h1", class_="h1_monhoc").text
        Title = soup.find("h2", class_="h2_monhoc").text
        lecture = soup.find("span", class_="money").text
        Code = soup.find("div", class_="col_navi").text
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Nguvan/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Nguvan/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Nguvan/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

def get_sinhhoc():
    dem = 0
    cau = 0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
    #     list_link = json.loads(j.read())
    # for link in list_link:
    products_data = pd.read_csv(r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/baitap123url/sinhhoc.csv')
    for link in tqdm(products_data['link'].tolist()):
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
        sleep(1)
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@onclick="delete_cookie_lambai();"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()

        order = soup.find("div", string_="Số câu hỏi: ").text
        time = soup.find("div", string_="Thời gian làm bài: " ).text
        subject = soup.find("h1", class_="h1_monhoc").text
        Title = soup.find("h2", class_="h2_monhoc").text
        lecture = soup.find("span", class_="money").text
        Code = soup.find("div", class_="col_navi").text
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Sinhhoc/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Sinhhoc/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Sinhhoc/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

def get_tienganh():
    dem = 0
    cau = 0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
    #     list_link = json.loads(j.read())
    # for link in list_link:
    products_data = pd.read_csv(r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/baitap123url/tienganh.csv')
    for link in tqdm(products_data['link'].tolist()):
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
        sleep(1)
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@onclick="delete_cookie_lambai();"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()

        order = soup.find("div", string_="Số câu hỏi: ").text
        time = soup.find("div", string_="Thời gian làm bài: " ).text
        subject = soup.find("h1", class_="h1_monhoc").text
        Title = soup.find("h2", class_="h2_monhoc").text
        lecture = soup.find("span", class_="money").text
        Code = soup.find("div", class_="col_navi").text
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Tienganh/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Tienganh/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Tienganh/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

def get_toanhoc():
    dem = 0
    cau = 0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
    #     list_link = json.loads(j.read())
    # for link in list_link:
    products_data = pd.read_csv(r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/baitap123url/baitap123.csv')
    for link in tqdm(products_data['link'].tolist()):
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
        sleep(1)
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@onclick="delete_cookie_lambai();"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()

        order = soup.find("div", string_="Số câu hỏi: ").text
        time = soup.find("div", string_="Thời gian làm bài: " ).text
        subject = soup.find("h1", class_="h1_monhoc").text
        Title = soup.find("h2", class_="h2_monhoc").text
        lecture = soup.find("span", class_="money").text
        Code = soup.find("div", class_="col_navi").text
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Toanhoc/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Toanhoc/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Toanhoc/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

def get_vatly():
    dem = 0
    cau = 0
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    # with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
    #     list_link = json.loads(j.read())
    # for link in list_link:
    products_data = pd.read_csv(r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/baitap123url/vatly.csv')
    for link in tqdm(products_data['link'].tolist()):
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
        sleep(1)
        browser.get(link)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        browser.find_element_by_xpath('//*[@onclick="delete_cookie_lambai();"]').click()
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()

        order = soup.find("div", string_="Số câu hỏi: ").text
        time = soup.find("div", string_="Thời gian làm bài: " ).text
        subject = soup.find("h1", class_="h1_monhoc").text
        Title = soup.find("h2", class_="h2_monhoc").text
        lecture = soup.find("span", class_="money").text
        Code = soup.find("div", class_="col_navi").text
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Vatly/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Vatly/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Vatly/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

def get_gdcd():
    dem = 0
    cau = 0
    browser.get('https://www.baitap123.com/')
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    wait = WebDriverWait(browser, 2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
    sleep(1)
    try:
        browser.find_element_by_xpath('//*[@id="fb-closebox"]').click()
    except:
        pass
    with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    with open(r'/Get_questions_iq/Get_questions_iq/spiders/JSon/questiontext.json', 'r') as j:
    #with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\link.json', 'r') as j:
         list_link = json.loads(j.read())
    for link in list_link:
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\baitap123url\gdcd.csv')
    # for link in tqdm(products_data['link'].tolist()):

        browser.get(link["link"])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        try:
            browser.find_element_by_link_text("Làm bài trắc nghiệm").click()
        except:
            continue
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        # browser.quit()
        try:
            order = soup.find("div", string_="Số câu hỏi: ").text
            time = soup.find("div", string_="Thời gian làm bài: " ).text
            subject = soup.find("h1", class_="h1_monhoc").text
            Title = soup.find("h2", class_="h2_monhoc").text
            lecture = soup.find("span", class_="money").text
            Code = soup.find("div", class_="col_navi").text
        except:
            continue
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
        data["Title"] = Title
        data["Code"] = Code
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
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/GDCD/iamge_ask/'
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

            order = re.findall(r'\d+', order)
            time = re.findall(r'\d+',time )
            #time = int(str(time)[:2])
            list_answer = []
            dict2 = {
                        'Id': cau,
                        'Order': int(order[0]),
                        'Duration': int(time[0]),
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
                        filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/GDCD/image_answer/'
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

                # def checkTrueFalse(s):
                #     if s.find("img", class_="imgTick"):
                #         return True
                #     else:
                #         return False

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

            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/GDCD/'
            print(filePath + filename)
            with open(filePath + filename, "w") as f:
            #with open(filename, "w") as f:
                f.write(data_string)
        except:
            pass
        cau = 0

get_gdcd()
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

