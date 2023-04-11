import re
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

name = "tuyensinh247"
def login():
    browser.get('https://tuyensinh247.com/')
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    wait = WebDriverWait(browser, 2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div[1]/div[1]/div/div[2]/ul/li[2]/a'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username_popup"]'))).send_keys("huynguyen474")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password_popup"]'))).send_keys("nguyenvanhuy")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@onclick="eLoginPopup();"]'))).click()
    sleep(1)
def get_tuyensinh247():
    dem =0
    cau =0
    login()
    with open(r'/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json', 'r', encoding='utf8') as outfile:
        data = json.load(outfile)
    with open(r'/Get_questions_iq/Get_questions_iq/spiders/JSon/tuyensinh247test.json', 'r') as j:
        list_link = json.loads(j.read())
    # products_data = pd.read_csv(r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\questIQ.csv')
    # list_link =  tqdm(products_data['link'].tolist())
    for link in list_link:
        browser.get(link["link"])
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        lecture = soup.find("span", class_="color-blue text-upercase size-24 text-center").text
        lecture = lecture.replace("(Có video chữa)", "")
        time_local = soup.find("p", class_="size-18 summury-info text-center").text
        timelst = re.findall(r'\d+', time_local)
        order = timelst[1]
        time = timelst[0]
        sleep(1)
        data["SubjectCode"] = None
        data["Title"] = "Title"
        data["Code"] = None
        data["ID"] = 123
        data["LectureCode"] = lecture

        browser.find_element_by_xpath('//*[@class="go-exam btn-onclick"]').click()
        browser.switch_to.window(browser.window_handles[1])
        browser.find_element_by_xpath('//*[@class=" btn-onclick"]').click()
        sleep(2)
        browser.find_element_by_xpath('//*[@class="  btn-onclick"]').click()
        browser.find_element_by_xpath('//*[@class="btn-onclick submit-exam"]').click()
        sleep(1)
        browser.find_element_by_xpath('//*[@class="submit-exam submit-finish-exam btn-onlick"]').click()
        wait = WebDriverWait(browser, 2)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="rank-table"]')))
        page_source= browser.page_source
        dapan_source = BeautifulSoup(page_source, 'lxml')

        List_of_source = dapan_source.find_all("div", class_="content-question")

        print(len(List_of_source))
        list_title = []
        for i in List_of_source:
            cau += 1
            title_decode = ''.join(map(str, i.contents))
            Lst_title_img = []
            Lst_title_img.clear()
            for p in i.find_all('p'):
                if p.find("img"):
                    title_local_img = p.find('img')["src"]
                    title_img = title_local_img
                    Lst_title_img.append(title_img)
            title_img = '_'.join(Lst_title_img)
            # title_local = i.find(lambda tag: tag.name == 'p' and not tag.attrs)
            # try:
            #
            #     if title_local.find("img"):
            #         title = title_local.text + '' + title_local.find("img").attrs["src"]
            #     else:
            #         title = title_local.text
            #     if title != '\n ':
            #         title = title
            # except:
            #     pass
            try:
                if i.find("img"):
                    img_url = i.find("img")["src"]
                    img_head_ask = requests.get(img_url)
                    img_name_ask = lecture + " CauSo" + str(cau) + '.png'
                    filepath = r'/Get_questions_iq/Get_questions_iq/spiders/tuyensinh247/image/image_answer/'
                    with open(filepath + img_name_ask, "wb") as im_h:
                        im_h.write(img_head_ask.content)
            except:
                continue

            list_answer =[]
            dict2 = {
                'Id': cau,
                'Order': order,
                'Duration': time,
                'Unit': 'MINUTE',
                'Mark': 10,
                'Content': title_decode,
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
                        'Url': title_img,
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

            answer_posi = i.find('ul')
            answer_local = answer_posi.find_all('li')
            print(len(answer_local))
            for s in answer_local:
                answer = s.find("a")
                if s.find("img"):
                    answer_decode = ''.join(map(str, answer.contents))
                    answer_get = answer.find("img").attrs["src"]
                else:
                    answer_decode = ''.join(map(str, s.contents))
                    answer_get = answer.text
                    # answer_get = answer_get.replace("                           ", "")
                    #answer_get = answer_get.replace("\n", " ")
                    # if answer_get != '    ':
                    #     answer_get = answer_get
                try:
                    if answer.find("img"):
                        img_ans_url = answer.find("img")['src']
                        img_head_ans = requests.get(img_ans_url)
                        img_name_ans = lecture + " CauTraLoi" + str(cau) + '.png'
                        filepath = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\tuyensinh247\image\iamge_ask/'
                        with open(filepath + img_name_ans, "wb") as im:
                            im.write(img_head_ans.content)
                except:
                    pass

                def checkTrueFalse(s):
                    if s.find("li", style_="border:2px solid red;border-radius: 10px;"):
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
                    'Answer': answer_decode,
                    'Type': checkType(answer),
                    'ContentDecode': answer_get,
                    'IsAnswer': checkTrueFalse(answer)
                }

                list_answer.append(answerdata)
                #print("cau hoi: " + str(len(list_answer)))

        print(len(list_title))
        #print('socau: ' + str(len(list_title)))
        data["Object"]["details"] = list_title
        data_string = json.dumps(data, indent=4)
        data_string = data_string.lstrip()
        dem += 1
        lecture = lecture.replace("\n", "")
        lecture = lecture.replace("           ", "")
        # filename = lecture + '_' + str(dem) + '.json'
        filename = str(dem) + '.json'
        filePath = r'/Get_questions_iq/Get_questions_iq/spiders/tuyensinh247/'
        print(filePath + filename)
        with open(filePath + filename, "w") as f:
            f.write(data_string)
        cau = 0
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

get_tuyensinh247()


