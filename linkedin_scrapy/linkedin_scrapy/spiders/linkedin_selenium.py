# coding=utf8
# -*- coding: utf-8 -*-
import asyncio
import json
import sys
from datetime import datetime
from time import sleep

import requests
import websockets
from docx import Document
from selenium import webdriver

name = 'CorelinkedinSpider'
options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
# options.add_argument('disable_infobars')
options.add_argument("start-maximized")
# options.add_argument('--headless')
browser = webdriver.Edge(executable_path=r'C:\Users\Admin 3i\PycharmProjects\Source\msedgedriver.exe', options=options)

URL = 'ws://127.0.0.1:9097'


async def login(tk, mk):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Login!')
        browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        user = browser.find_element_by_xpath('//*[@name="session_key"]')
        user.send_keys(tk)
        sleep(2)
        pwd = browser.find_element_by_xpath('//*[@name="session_password"]')
        pwd.send_keys(mk)
        sleep(2)
        browser.find_element_by_xpath('//*[@type="submit"]').click()


async def linkedin_auto_post(content, hashtag, media):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Post!')
        browser.find_element_by_xpath(
            '//*[@class="artdeco-button artdeco-button--muted artdeco-button--4 artdeco-button--tertiary ember-view share-box-feed-entry__trigger"]').click()
        sleep(2)
        text_box = browser.find_element_by_xpath('//*[@aria-label="Text editor for creating content"]')
        text_box.send_keys(content + '\n' + hashtag + '\n' + media)

        sleep(2)
        browser.find_element_by_xpath('//*[@class="share-box_actions"]').click()
        await ws.send('Post Done!')
        sleep(2)


async def linkedin_comment(post, content):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Comment!')
        for i in range(len(post)):
            browser.get(post[i])
            await ws.send('LinkPost: ' + post[i])
            sleep(2)
            text_box = browser.find_element_by_xpath('//*[@aria-placeholder="Add a comment…"]')
            text_box.send_keys(content)
            sleep(2)
            browser.find_element_by_xpath(
                '//*[@class="comments-comment-box__submit-button mt3 artdeco-button artdeco-button--1 artdeco-button--primary ember-view"]').click()
            await ws.send('Comment done! ' + content)
            sleep(2)


async def linkedin_get_content(post):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start get content!')
        content = []
        for i in range(len(post)):
            browser.get(post[i])
            content.append(post[i])
            await ws.send('Post link: ' + post[i])
            sleep(2)
            data = browser.find_element_by_xpath('//*[@class="feed-shared-update-v2__description-wrapper"]')
            text = data.text
            content.append(text)
            img = browser.find_element_by_xpath(
                '//*[@class="ivm-view-attr__img--centered feed-shared-image__image feed-shared-image__image--constrained lazy-image ember-view"]').get_attribute(
                "src")
            print(img)
        document = Document()
        endtime = datetime.now()
        end_time = endtime.strftime("%H:%M:%S")
        end_time = end_time.replace(":", "_")
        filename = 'getlinkedincontent' + end_time
        print(content)
        for value in content:
            document.add_paragraph(value)
        content.save(r'C:\Users\Admin 3i\PycharmProjects\Source\linkedin_scrapy' + filename + '.docx')
        url_upload = "https://dieuhanh.vatco.vn/MobileLogin/InsertFile"
        response_upload = requests.post(url_upload,
                                        data={"CateRepoSettingId": 2247, "CreatedBy": "phancuoc_cntt_3i"}, files={
                "fileUpload": (
                    filename + '.docx',
                    open(r'C:\Users\Admin 3i\PycharmProjects\Source\linkedin_scrapy/' + filename + '.docx', 'rb'),
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
        if response_upload.ok:
            print("Upload completed successfully!")
            print(response_upload.text)
        else:
            print("Something went wrong!")
        await ws.send('Upload Done')


async def linkedin_like(post):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Like!')
        for i in range(len(post)):
            browser.get(post[i])
            await ws.send('Like post: ' + post[i])
            sleep(2)
            browser.find_element_by_xpath('//*[@type="like-icon"]').click()
            await ws.send('Liked!')
            sleep(2)


async def linkedin_unlike(post):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Unlike!')
        for i in range(len(post)):
            browser.get(post[i])
            await ws.send('Unlike post: ' + post[i])
            sleep(2)
            browser.find_element_by_xpath(
                '//*[@class="reactions-react-button feed-shared-social-action-bar__action-button"]').click()
            sleep(2)


profile = ['https://www.linkedin.com/in/linhthaiofficial/', 'https://www.linkedin.com/in/jehakjerrylee/']


async def listen():
    ws_connect = websockets.connect('ws://127.0.0.1:9097', ping_interval=None)
    async with ws_connect as wb:
        while True:
            param = await wb.recv()
            print(param)
            if 'PassWord' in param:
                data = json.loads(param)
                tk = data['UserName']
                mk = data['PassWord']
                asyncio.create_task(login(tk, mk))
            if 'Start post content' in param:
                data = json.loads(param)
                content = data['Start post content']['content']['content']
                media = data['Start post content']['content']['Image']
                hashtag = "data['Post']['Main_post']['hashtag']"
                asyncio.create_task(linkedin_auto_post(content, hashtag, media))
            if 'Get' in param:
                data = json.loads(param)
                post = data['Get']['post']
                asyncio.create_task(linkedin_get_content(post))
            if 'Like' in param:
                data = json.loads(param)
                post = data['Like']['post']
                asyncio.create_task(linkedin_like(post))
            if 'Unlike' in param:
                data = json.loads(param)
                post = data['Unlike']['post']
                asyncio.create_task(linkedin_unlike(post))
            if 'Stop' in param:
                # flagstop = True
                browser.quit()
                sys.exit()


async def main():
    task_1 = asyncio.create_task(listen())
    await task_1


if __name__ == '__main__':
    asyncio.run(main())
