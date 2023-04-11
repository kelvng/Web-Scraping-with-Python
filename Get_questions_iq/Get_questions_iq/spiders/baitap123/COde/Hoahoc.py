import sys
from datetime import datetime
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
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#khai bao broswer
options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Edge(executable_path=r'C:\Users\Admin\PycharmProjects\Source\msedgedriver.exe',
                               options=options)

# class baitap123(scrapy.Spider):
#     name = "baitap123"
#     allowed_domains = ['https://www.baitap123.com/']

name = "hoahocbaitap123"
domain = 'baitap123.com'
def login():
    browser.get('https://www.baitap123.com/')
    page_source = browser.page_source
    wait = WebDriverWait(browser, 2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
    sleep(1)

def get_hoahoc():
    global answer
    dem = 0
    cau = 0
    demdownload = 0
    login()
    with open(r"C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\new.json", 'r', encoding="utf8") as outfile:
        data = json.load(outfile)
    with open(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\JSon\jsontestbaitap123\hoahoctest.json', 'r') as j:
         list_link = json.loads(j.read())
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\baitap123url\tracnghiemall.csv')
    # list_link = tqdm(products_data['link'].tolist())
    products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Hoahoc\test.csv')
    list_link = tqdm(products_data['link'].tolist())
    list_url =[]
    for link in list_link:
        list_url = []
        list_url.append(link)
        browser.get(link)
        #browser.get(link['link'])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        try:
            browser.find_element_by_link_text("Làm bài trắc nghiệm").click()
        except:
            pass
        sleep(1)
        page_source = browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        order = soup.find("div", class_="xacnhan_top").text
        time = soup.find('div', class_="xacnhan_bottom").text
        lecture = soup.find("span", class_="money").text  #
        subject = order.split("\n")[1]  # subject
        Title = order.split("\n")[2]  # title

        data["Domain"] = domain
        data["Url"] = list_url
        data["TimeScan"] = "Endtimenow"
        data["DownloadFile"] = "numbfiledown"
        data["Datastorage"] = "file size"

        data["SubjectCode"] = subject
        data["Title"] = Title
        data["Code"] = "Code"
        data["ID"] = None
        data["LectureCode"] = lecture
        list_title = []
        List_of_source = dapan_source.findAll(True, {
            'class':['lb_question_item pagi_page_1', 'lb_question_item pagi_page_2',
                     'lb_question_item pagi_page_3', 'lb_question_item pagi_page_4',
                     'lb_question_item pagi_page_5', 'lb_question_item pagi_page_6']})

        for i in List_of_source:
            cau += 1
            title_local = i.find("div", class_="lb_cauhoi")
            try:
                if title_local.find("img"):
                    img_url = title_local.find("img")["src"]
                    img_head_ask = requests.get(img_url)
                    img_name_ask =subject + "-"+lecture + " CauSo" + str(cau) + '.png'
                    filepath = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Hoahoc\iamge_ask/'
                    with open(filepath + img_name_ask, "wb") as im_h:
                        im_h.write(img_head_ask.content)
            except:
                continue
            if  title_local.find("img"):
                title = title_local.text +''+ title_local.find("img").attrs["src"]
            else:
                title = title_local.text
                if title != '\n ':
                    title = title

            # numask
            numask = time.split("\n")[1]
            numask = re.findall('\d+', numask)

            # duration
            timeask = time.split("\n")[2]
            timeask = re.findall("\d+", timeask)

            list_answer = []
            dict2 = {
                'Id': cau,
                'Order': int(numask[0]),
                'Duration': int(timeask[0]),
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
                        img_name_ans =subject + "-"+lecture + " CauTraLoi" + str(cau) + '.png'
                        filepath = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Hoahoc\image_answer/'
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
                    answer_get = answer_get.replace("                                   ", "")
                    answer_get = answer_get.replace("\n", " ")
                    if answer_get != '    ':
                        answer_get = answer_get
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
        data_string = json.dumps(data, indent=4)
        data_string = data_string.lstrip()

        dem += 1
        filename =subject + "-"+ lecture + '_' + str(dem) + '.json'

        filePath = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Hoahoc/'
        print(filePath + filename)
        with open(filePath + filename, "w") as f:
        #with open(filename, "w") as f:
            f.write(data_string)
        cau = 0
    print(list_url)
    browser.close()
    end = datetime.now()

    end_time = end.strftime("%H:%M:%S")
    print("Current Time =",end_time)
get_hoahoc()
sys.exit()