import asyncio
import json
import os
import sys
from telnetlib import EC
from bs4 import BeautifulSoup
import pandas as pd
import websockets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import numpy as np
import random
from pywinauto.application import Application

from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from pynput.keyboard import Key, Controller
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

# constants
from selenium.webdriver.common import action_chains
import random

options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
driver_path = r'C:\Users\Admin 3i\PycharmProjects\Source\msedgedriver.exe'
browser = webdriver.Edge(executable_path=driver_path, options=options)



URL = 'ws://127.0.0.1:9097'

async def login(tk,mk):
    browser.get('https://www.quora.com/')
    id = browser.find_element_by_xpath('//*[@name="email"]')
    id.send_keys(tk)
    pwd = browser.find_element_by_xpath('//*[@name="password"]')
    pwd.send_keys(mk)
    sleep(1)
    pwd.send_keys(Keys.ENTER)
    sleep(2)

async def quora_auto_post(option,content):
    if 'Post' in option:
        browser.find_element_by_xpath("//div[text()='Post']").click()
        await asyncio.sleep(1)
        # Click on 'Upload Video'
        post = browser.find_element_by_xpath('//*[@data-placeholder="Say something..."]')
        post.send_keys(content)
        await asyncio.sleep(1)
        browser.find_element_by_xpath("//div[text()='Post']").click()
        sleep(2)
        browser.switch_to.window(browser.window_handles[1])
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    if 'Ask' in option:
        browser.find_element_by_xpath("//div[text()='Post']").click()
        sleep(1)
        browser.find_element_by_xpath('//*[@class="q-flex qu-justifyContent--center qu-alignItems--center qu-py--small qu-borderBottom qu-borderColor--gray qu-borderWidth--retinaOverride qu-hover--bg--darken qu-borderTopRightRadius--medium"]').click()
        sleep(1)
        post = browser.find_elements_by_xpath('//*[@aria-haspopup="listbox"]')[0]
        #post = browser.find_element_by_xpath('//*[@class="q-flex qu-alignItems--center qu-bg--white qu-borderColor--gray qu-hover--borderColor--blue qu-hover--zIndex--1 qu-borderBottom qu-pb--small InputStyleWrapper___StyledFlex-sc-1d0740s-0 bjNfxn"]')
        post.send_keys(content)
        sleep(1)
        browser.find_element_by_xpath('//*[@class="q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 kjJTYv puppeteer_test_modal_submit  qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-bg--blue qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"]').click()
        sleep(2)
        browser.find_elements_by_xpath('//*[@class="q-click-wrapper ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 laIUvT puppeteer_test_modal_cancel  qu-active--bg--darken qu-active--textDecoration--none qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--bg--darken qu-hover--textDecoration--none"]')[1].click()
        print(1)
        sleep(1)
        browser.find_element_by_xpath('//*[@class="q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 kjJTYv puppeteer_test_modal_submit  qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-bg--blue qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"').click()
        print(2)
        sleep(1)
        y = browser.find_element_by_xpath('//*[@class="q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 kjJTYv puppeteer_test_modal_submit  qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-bg--blue qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"]')
        y[2].click()
        print(y)
async def quora_auto_comment(post, content, keyword):

    for j in keyword:

        pass

    for i in post:
        browser.get(i)

        #browser.find_element_by_xpath('//*[@name="Comment"]').click()
        await asyncio.sleep(2)
        # Click on 'Upload Video'
        post = browser.find_element_by_xpath('//*[@data-placeholder="Add a comment..."]')
        post.send_keys(content)
        await asyncio.sleep(1)
        browser.find_element_by_xpath("//div[text()='Add Comment']").click()

def infinite_scroll(limit=False):
    count = 0
    while count<limit:
        try:
            current = browser.page_source
            browser.execute_script ("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep (2)
            new = browser.page_source
            urls = len (browser.find_elements_by_class_name ("question_link"))
            if current == new:
                return
            if limit and limit <= urls:
                return
        except Exception as e:
            print(e)
        count += 1

async def quora_auto_upvote(post):
    #async with websockets.connect(URL, ping_interval=None) as ws:
        i = 0
        while i < len(post):
            print("Start like")
            browser.get(post[i])
            await asyncio.sleep(3)
            browser.find_element_by_xpath('//*[@name="Upvote"]').click()
            #await ws.send('Follow: ' + str())
            i += 1

async def quora_auto_downvote(post):
    #async with websockets.connect(URL, ping_interval=None) as ws:
        i = 0
        while i < len(post):
            print("Start like")
            browser.get(post[i])
            await asyncio.sleep(3)
            browser.find_element_by_xpath('//*[@name="Downvote"]').click()
            #await ws.send('Follow: ' + str())
            i += 1

#check lateter
async def quora_auto_follow_topic(name,scroll_count):
    for j in name:
        print(j)
        sleep(2)
        post = browser.find_element_by_xpath('//*[@placeholder="Search Quora"]')
        post.send_keys(Keys.CONTROL, 'a')
        post.send_keys(Keys.DELETE)
        post.send_keys(j)
        sleep(2)
        post.send_keys(Keys.ENTER)
        browser.find_elements_by_xpath('//*[@class="q-box qu-pl--medium qu-pr--medium qu-hover--cursor--pointer qu-hover--bg--darken qu-tapHighlight--none qu-display--flex qu-alignItems--center"]')[4].click()
        sleep(2)
        #infinite_scroll(scroll_count)
        #get url
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        list_follow = browser.find_elements_by_xpath('//*[@class="q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 dczqNg   qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-bg--blue_light qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"]')

        print(list_follow)
        for i in list_follow:
            i.click()
            #browser.find_element_by_xpath('//*[@class="q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 dczqNg   qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-bg--blue_light qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"]').send_keys(Keys.PAGE_DOWN)
            sleep(1)
            pass

        # lấy content của web rồi pass qua beatifulsoup
        # page_source = browser.page_source
        # soup = bs(page_source, 'lxml')
        # links = []
        # # tìm tất cả đường link của các group
        # page_groups = soup.find("div", {"id": "mainContent"})
        # for s in page_groups.find_all('a'):
        #     print(s)
        #     try:
        #         link = s['href']
        #         # members = s['/html/body/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/span/div/div[3]/a']
        #         if 'topic' in link:
        #             links.append(link)
        #         # links.append(members)
        #     except:
        #         pass
        # for i in range(len(links)):
        #     try:
        #         print("Start invite friends to group")
        #         a = links[i]
        #         browser.get(links[i])
        #         sleep(3)
        #         browser.find_element_by_xpath("//div[text()='Follow']").click()
        #         #await ws.send('Follow: ' + str(a))
        #         await asyncio.sleep(1)
        #     except:
        #         print(1)
async def quora_auto_unfollow_topic(name):
    for j in name:
        print(j)
        sleep(2)
        post = browser.find_element_by_xpath('//*[@placeholder="Search Quora"]')
        post.send_keys(Keys.CONTROL, 'a')
        post.send_keys(Keys.DELETE)
        post.send_keys(j)
        sleep(2)
        post.send_keys(Keys.ENTER)

        sleep(2)
        # for i in range(0, 5):
        #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(3)
        list_follow = browser.find_elements_by_xpath('//*[@class="q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 ilbVnc  puppeteer_test_pressed qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"]')
        print(list_follow)
        for i in list_follow:
            i.click()
            #browser.find_element_by_xpath('//*[@class="q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 dczqNg   qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-bg--blue_light qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"]').send_keys(Keys.PAGE_DOWN)
            sleep(1)
            pass
    pass


async def quora_auto_share(post,content):
    for i in post:
        browser.get(i)
        sleep(2)
        browser.find_element_by_xpath('//*[@aria-label="Share"]').click()
        sleep(2)

        keyboard = Controller()
        keyboard.type(content)
        sleep(1)
        browser.find_element_by_xpath('//*[@class="q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 kjJTYv puppeteer_test_modal_submit  qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-bg--blue qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"]').click()
        sleep(2)
        browser.switch_to.window(browser.window_handles[1])
        browser.close()
        browser.switch_to.window(browser.window_handles[0])


async def listen():
    ws_connect = websockets.connect('ws://127.0.0.1:9097', ping_interval=None)
    async with ws_connect as wb:
        while True:
                param = await wb.recv()

                if "Login" in param:
                    data = json.loads(param)
                    print(type(data))
                    tk = data['Login']['Username']
                    mk = data['Login']['Password']
                    asyncio.create_task(login(tk,mk))

                if "Post" in param:
                    print(1)
                    data = json.loads(param)
                    content = data['Post']['content']
                    option = data['Post']['option']
                    await asyncio.sleep(5)
                    asyncio.create_task(quora_auto_post(option,content))
                if "comment" in param:
                    print(1)
                    data = json.loads(param)
                    content = data['comment']['content']
                    post = data['comment']['Post']
                    await asyncio.sleep(5)
                    asyncio.create_task(quora_auto_comment(post,content))
                if "follow" in param:
                    print(1)
                    data = json.loads(param)
                    name = data['follow']['topic']['name']
                    await asyncio.sleep(5)
                    asyncio.create_task(quora_auto_follow_topic(name))
                if "unFollow" in param:
                    print(1)
                    data = json.loads(param)
                    name = data['unFollow']['topic']['name']
                    await asyncio.sleep(5)
                    asyncio.create_task(quora_auto_unfollow_topic(name))
                if "Upvote" in param:
                    print(1)
                    data = json.loads(param)
                    post = data['Upvote']['post']
                    await asyncio.sleep(5)
                    asyncio.create_task(quora_auto_upvote(post))
                if "DownVote" in param:
                    print(1)
                    data = json.loads(param)
                    post = data['DownVote']['post']
                    await asyncio.sleep(5)
                    asyncio.create_task(quora_auto_downvote(post))

                if "share" in param:
                    print(1)
                    data = json.loads(param)
                    post = data['share']['Post']
                    content = data['share']['content']
                    await asyncio.sleep(5)
                    asyncio.create_task(quora_auto_share(post,content))
                # if 'Stop' in param:
                #     # flagstop = True
                #     browser.quit()
                #     sys.exit()
async def main():
    task_1 = asyncio.create_task(listen())
    await task_1

if __name__ == '__main__':
    asyncio.run(main())