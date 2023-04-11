# coding=utf8
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import asyncio
import json
import os
import re
import uuid
from datetime import datetime
from time import sleep
import requests
import scrapy
import websockets
from bs4 import BeautifulSoup
from docx import Document
from selenium import webdriver
import sys
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import pandas as pd
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

time = datetime.now()
current_time = time.strftime("%H:%M:%S")
print("Current Time =", current_time)

# khai bao broswer
options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Edge(executable_path=r'/msedgedriver.exe',
                         options=options)
time = datetime.now()
current_time = time.strftime("%H:%M:%S")
print("Current Time =", current_time)

# khai bao broswer
options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Edge(executable_path=r'/msedgedriver.exe',
                         options=options)

time = datetime.now()
start_time = time.strftime("%H:%M:%S")
print("Current Time =", start_time)

list_child_url = []
list_url = []
# data json for summary
with open(r'/Get_questions_iq/Get_questions_iq/spiders/JSon/summary.json', 'r', encoding='utf8') as push:
    datapush = json.load(push)
# data json for
with open(r"/Get_questions_iq/Get_questions_iq/spiders/JSon/new.json", 'r',
          encoding="utf8") as outfile:
    data = json.load(outfile)
URL = 'ws://127.0.0.1:9091'

def outer_func():
    class url_obj:

        def __init__(self, url, iscan, deep, selector, deepscan, linkadd):
            self.url = url
            self.iscan = iscan
            self.deep = deep
            self.selector = selector
            self.deepscan = deepscan
            self.linkadd = linkadd
        Idx = 0
        chk = 0

        # Hàm kiểm tra link đã tồn tại trong list chưa
        def chk_link_exist(self, link):
            for obj in list_child_url:
                if (obj.url == link):
                    return 1
            return 0

        # Hàm quét và lấy các link con từ link mẹ
        def Extract_Url(self, url, deep, deepscan, linkadd):
            try:
                # Độ sâu của link mẹ là 1, link con = link mẹ +1
                if deep <= deepscan:
                    self.deep = deep
                    req = requests.get(url)
                    html = req.text
                    soup = BeautifulSoup(html, 'html.parser')
                    LstLink = soup.find('body')
                    for s in LstLink.find_all('a'):
                        try:
                            link = s['href']
                            if 'http' not in link:
                                link = linkadd + link

                                if self.chk_link_exist(link) == 0:
                                    url = link
                                    iscan = 0
                                    deep = self.deep + 1
                                    list_child_url.append(
                                        url_obj(url, iscan, deep, self.selector, self.deepscan,
                                                self.linkadd))
                            else:
                                if linkadd in link:
                                    if self.chk_link_exist(link) == 0:
                                        url = link
                                        iscan = 0
                                        deep = self.deep + 1
                                        list_child_url.append(
                                            url_obj(url, iscan, deep, self.selector, self.deepscan,
                                                    self.linkadd))
                                else:
                                    print('Strange link!')
                                    pass
                        except:
                            pass
            except:
                print('link fail')
                pass
        def check_link(self, url):
            browser.get(url)
            sleep(2)
            page_source = browser.page_source
            if browser.find_element_by_xpath("Làm bài trắc nghiệm"):
                return 0
            else:
                return 1
        def login(self,linkadd):
            browser.get(linkadd)
            wait = WebDriverWait(browser, 2)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="ic_login"]'))).click()
            # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("familytotoro257")
            # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("anhhuyc3")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_user"]'))).send_keys("smart-work ")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dn_pass"]'))).send_keys("Langnghiem79")
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="btn btn_login hvr-grow"]'))).click()
            # browser.find_element_by_xpath('//*[@id="fb-closebox"]').click()
            sleep(1)

        def get_question(self, url, selector, linkadd):
            demdownload = 0
            dem = 0
            cau = 0
            self.login(linkadd)
            global title, title_img
            filedownload = []
            browser.get(url)
            list_url.append(url)
            page_source = browser.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            try:
                browser.find_element_by_link_text("Làm bài trắc nghiệm").click()
                sleep(1)
            except:

                pass
            order = soup.find("div", class_="xacnhan_top").text
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
            page_source = browser.page_source
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
                    'Id': None,
                    'Order': cau,
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
                            'Check': checkQuestionmedia()
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
                            'Check': checkQuestionmedia()
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
                                filepath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/image_all/Answer/'
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
                        'IsAnswer': False
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
                    "url": url,
                    "fileDownloadname": list_filedownload,
                    "status": checkstatus()
                }
                filedownload.append(filedownloadjson)
                dem += 1
                # save json
                filename = subject + "-" + lecture + '_' + str(dem) + '.json'
                # filePath = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\json_all/'
                filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Tinhcach/'
                print(filePath + filename)
                with open(filePath + filename, "w") as f:
                    f.write(data_string)
                cau = 0
                sleep(1)
            datapush['FileDownloadJson'] = filedownload
            datapush['DownloadFile'] = demdownload

        def up_load(self):

            endtime = datetime.now()
            end_time = endtime.strftime("%H:%M:%S")
            print("Current Time =", end_time)
            # filePathsave = r'C:\Users\Admin\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\baitap123\Toanhoc'
            datapush['TimeScan'] = end_time
            datapush['BotCode'] = 'domain'
            datapush['Url'] = list_url
            filename = name + '_' + 'summary' + '.json'
            datapush_obj = json.dumps(datapush, indent=4)
            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Toanhoc/summary/'
            with open(filePath + filename, 'w') as summary:
                summary.write(datapush_obj)
            # check size
            size = 0
            filePath = r'/Get_questions_iq/Get_questions_iq/spiders/baitap123/Toanhoc'
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

        async def main(self):
            Idx = 0
            len_list = len(list_child_url)
            await asyncio.sleep(10)
            while Idx < len_list:
                async with websockets.connect(URL, ping_interval=None) as ws:
                    try:
                        self.Extract_Url(list_child_url[Idx].url, list_child_url[Idx].deep,
                                         list_child_url[Idx].deepscan, list_child_url[Idx].linkadd)
                    except:
                        pass
                    try:
                        self.get_question(list_child_url[Idx].url, list_child_url[Idx].selector, list_child_url[Idx].linkadd)
                    except:
                        pass
                    await ws.send(str(datetime.now()) + ": " + list_child_url[Idx].url)
                    Idx = Idx + 1
                    len_list = len(list_child_url)
                    print(len_list)
                    print(Idx)
                    pass

            print(1)
            time = datetime.now()
            end_time = time.strftime("%H:%M:%S")

            self.up_load()

    async def initspider(url, selector, deepscan, linkadd):
        list_child_url.append(url_obj(url, 0, 1, selector, deepscan, linkadd))
        object = url_obj(url, 0, 1, selector, deepscan, linkadd)
        await asyncio.sleep(5)
        asyncio.create_task(object.main())

    async def listen():
        ws_connect = websockets.connect('ws://127.0.0.1:9091', ping_interval=None)
        my_task = None
        async with ws_connect as wb:
            await wb.send('Spider running!')
            while True:
                param = await wb.recv()
                if "Url" in param:
                    data = json.loads(param)
                    print(data)
                    deepscan = data['DeepScan']
                    param1 = data['Url']
                    selector = data['ConfigSelectorJson']
                    selector = json.loads(selector)
                    BotCode = data['BotCode']
                    botcode.append(BotCode)
                    addurl = data['Url']
                    my_task = asyncio.create_task(initspider(param1, selector, deepscan, addurl))
                if 'Stop domain' in param:
                    # flagstop = True
                    # sys.exit()
                    if my_task:
                        print('Stop task')
                        my_task.cancel()
                        break
                    # content.clear()
                    # list_child_url.clear()
                    # url_scan.clear()
                    # scancontenturl.clear()
                    # botcode.clear()
                print("hearing")
            print("Stop async with ws_connect")
        print('Stop listen function')

    async def main():
        task_1 = asyncio.create_task(listen())
        await asyncio.sleep(0.250)
        await task_1

    # async def forever():
    #     while True:
    #         await main()
    loop = asyncio.get_event_loop()

    def startTask():
        try:
            loop.run_until_complete(main())
        except asyncio.CancelledError:
            print("some error but still fine")
        finally:
            print("live again")
            startTask()

    startTask()


class Myspider(scrapy.Spider):
    name = 'CoreEduSpider'
    some_attribute = "Yes|No"
    print("hello world !")
    outer_func()




