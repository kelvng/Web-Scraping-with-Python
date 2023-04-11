# coding=utf8
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import ast
import json
import os
from time import sleep
import docx
import scrapy
import websockets
import asyncio
import sys
import requests
from bs4 import BeautifulSoup
from docx import Document
from datetime import datetime

from docx.enum.dml import MSO_THEME_COLOR_INDEX

time = datetime.now()
start_time = time.strftime("%H:%M:%S")
print("Current Time =", start_time)

list_child_url = []
url_scan = []
# mảng chứa lisr url và content text abc
content = []
scancontenturl = []
botcode = []
Lst_scan_url = []

URL = 'https://thuvienstem-steam.com/'


def outer_func():
    class url_obj:

        def __init__(self, url, iscan, deep, deepscan, linkadd):
            self.url = url
            self.iscan = iscan
            self.deep = deep
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
                                        url_obj(url, iscan, deep, self.deepscan,
                                                self.linkadd))
                            else:
                                if linkadd in link:
                                    if self.chk_link_exist(link) == 0:
                                        url = link
                                        iscan = 0
                                        deep = self.deep + 1
                                        list_child_url.append(
                                            url_obj(url, iscan, deep, self.deepscan,
                                                    self.linkadd))
                                else:
                                    print('Strange link!')
                                    pass
                        except:
                            pass
            except:
                print('link fail')
                pass


        def GetContent(self, url):
            url = url
            Lst_scan_url.append(url)

        def save_file(self, document):
            filename = botcode[0] + '.docx'
            file_path = filename
            document.save(file_path)
            # r'C:\Users\Admin\PycharmProjects\Source\DomainManagement\DomainManagement\save\url1.docx')
            url_upload = "https://dieuhanh.vatco.vn/MobileLogin/InsertFile"
            # url_upload = resp_json['DataStoragePath']

            response_upload = requests.post(url_upload, data={"CateRepoSettingId": 2247, "CreatedBy": "huynv_cntt_3i"},
                                            files={
                                                "fileUpload": (
                                                    filename,
                                                    open(
                                                        file_path,
                                                        'rb'),
                                                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
            if response_upload.ok:
                print("Upload completed successfully!")
                print(response_upload.text)
                sleep(4)
                os.remove(file_path)
            else:
                print("Something went wrong!")

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
                        self.GetContent(list_child_url[Idx].url)
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
            urlscan_json = json.dumps(url_scan)
            # data["UrlScanJson"] = urlscan_json
            # data["endtime"] = end_time

            data = {
                'SessionCode': botcode[0] + end_time,
                'StartTime': start_time,
                'EndTime': end_time,
                'UrlScanJson': urlscan_json,
                'FileDownloadJson': 'url1.docx',
                'NumOfFile': 1,
                'FileResultData': '',
                'NumPasscap': '',
                'UserIdRunning': '001',
                'Ip': '1',
                'Status': 'active',
                'BotCode': botcode[0],
                'TimeScan': '',
                'CreatedBy': 'admin',
            }
            url_upload = "https://dieuhanh.vatco.vn/PythonCrawler/InsertCrawlerRunningLog"
            resp = requests.post(url_upload, data=data)
            if resp.ok:
                print("Upload completed successfully!")
                print(resp.text)
            else:
                print("Something went wrong!")
            document = Document()
            print('Done. Start save text!')
            for value in Lst_scan_url:
                document.add_paragraph(value)

            self.save_file(document)
            content.clear()
            list_child_url.clear()
            url_scan.clear()
            scancontenturl.clear()
            botcode.clear()
            Lst_scan_url.clear()
            async with websockets.connect(URL, ping_interval=None) as ws:
                await ws.send('Write file and Finish!')

    async def initspider(url, deepscan, linkadd):
        list_child_url.append(url_obj(url, 0, 1, deepscan, linkadd))
        object = url_obj(url, 0, 1, deepscan, linkadd)
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
                    #url ='https://tailieu.vn'
                    BotCode = data['BotCode']
                    botcode.append(BotCode)
                    addurl = data['Url']
                    my_task = asyncio.create_task(initspider(param1, deepscan, addurl))
                if 'Stop domain' in param:
                    # flagstop = True
                    # sys.exit()
                    if my_task:
                        print('Stop task')
                        my_task.cancel()
                        break
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
    name = 'CoreWebSpider'
    some_attribute = "Yes|No"
    print("hello world !")
    outer_func()




