import asyncio
import json
import os
import sys
from telnetlib import EC
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import websockets
from pynput.keyboard import Key,Controller
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import numpy as np
import random
from pywinauto.application import Application

from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException
import time

from selenium.webdriver.common import action_chains
import random
from selenium import webdriver
from selenium_stealth import stealth
import undetected_chromedriver.v2 as uc

# # prefs = {"profile.default_content_setting_values.notifications" : 2}
# # options.add_experimental_option("prefs",prefs)

# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver_path = r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe'
# browser = uc.Chrome(executable_path=driver_path, options=options)
# options = webdriver.ChromeOptions()
# # options.add_argument("start-maximized")
# options.add_argument("start-maximized")
browser = uc.Chrome()

stealth(browser,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


def wait():
    return sleep(random.randint(4,6))

URL = 'ws://127.0.0.1:9097'

async def login(tk,mk):
# login to facebook
    browser.get("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    sleep(2)
    id = browser.find_element_by_xpath('//*[@type="email"]')
    id.send_keys(tk)
    sleep(3)
    browser.find_element_by_xpath('//*[@class="VfPpkd-vQzf8d"]').click()
    sleep(3)
    pwd = browser.find_element_by_xpath('//*[@type="password"]')
    pwd.send_keys(mk)
    sleep(2)
    browser.find_element_by_xpath('//*[@class="VfPpkd-vQzf8d"]').click()
    sleep(2)

async def youtube_auto_post(media, content):
    filepath = r'C:\Users\Public\Video1.mp4'
    # if title is not in data, return immediately
    # navigate to the upload page
    browser.get('https://studio.youtube.com/')
    sleep(2)
    # click on 'Create' button
    try:
        browser.find_element_by_xpath('//*[@id="dismiss-button"]').click()
    except:
        pass
    browser.find_element_by_id('upload-button').click()
    sleep(2)
    # Click on 'Upload Video'
    browser.find_element_by_xpath('//*[@id="select-files-button"]').click()

    await asyncio.sleep(1)
    sleep(2)
    upload_dialog = Application().connect(title_re='Open')

    upload_dialog.send_keys(filepath)
    wait()
    upload_dialog.window(title_re='Open').Open.click()

    browser.find_element_by_xpath(
        '//button[contains(text(), "Select from computer")]').click()
    sleep(2)
    upload_dialog = Application().connect(title_re='Open')
    sleep(1)

    item = browser.find_element_by_xpath('//*[@aria-label="Add a title that describes your video"]')
    item.send_keys(content)
    item.send_keys(Keys.CONTROL, Keys.ENTER)
    browser.find_element_by_xpath('//*[@name="VIDEO_MADE_FOR_KIDS_MFK"]').click()
    # Next
    browser.find_element_by_id('next-button').click()
    sleep(1)
    browser.find_element_by_id('next-button').click()
    browser.find_element_by_id('next-button').click()

    visibilities = ['PUBLIC', 'UNLISTED', 'PRIVATE']
    browser.find_element_by_xpath('//*[@name="' + visibilities[0] + '"]').click()
    # Done
    browser.find_element_by_id('done-button').click()


async def youtube_auto_comment(link, content):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start comment')
        browser.get('https://www.youtube.com/')
        for i in link:
            browser.get(i)
            await ws.send('comment in video:' + i)
            sleep(2)
            dem = 0
            while dem < 3:
                browser.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
                dem +=1
                sleep(1)
            sleep(2)
            element = browser.find_element_by_xpath('//*[@id="placeholder-area"]')
            actions = ActionChains(browser)
            actions.move_to_element(element).perform()
            browser.find_element_by_xpath('//*[@id="placeholder-area"]').click()
            sleep(2)
            item = browser.find_element_by_xpath('//*[@id="contenteditable-root"]')
            item.send_keys(content)
            item.send_keys(Keys.CONTROL, Keys.ENTER)
            await ws.send('comment done!')
            wait()
async def youtube_auto_subscribe(link):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start subcribe!')
        for i in link:
            browser.get(i)
            sleep(3)
            try:
                browser.find_element_by_css_selector('.ytd-subscribe-button-renderer').click()
                print(1)
                await ws.send('Subcribe post:' + i)
            except:
                pass

    #seach sub name
    """name= 'yt remix'
    search = browser.find_element_by_xpath('//*[@name="search_query"]')
    search.send_keys(name)
    search.send_keys(Keys.CONTROL, Keys.ENTER)
    await asyncio.sleep(2)
    browser.find_element_by_xpath("//yt-formatted-string[text()='Subscribe']").click()"""

    #browser.quit()
async def youtube_auto_unsubscribe(link):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start unsubcribe!')
        for i in link:
            browser.get(i)
                    # tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual
            sleep(3)
            browser.find_element_by_xpath('//*[@class="style-scope ytd-subscribe-button-renderer"]').click()
            try:
                sleep(1)
                browser.find_element_by_xpath('//*[@id="confirm-button"]').click()
                await ws.send('unsubcribe post' + i)
            except:
                wait()
async def youtube_auto_like(link):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Like!')
        for i in link:
            url = 'https://www.youtube.com/watch?v='+str(i['id'])
            browser.get(url)
            sleep(3)
            browser.find_element_by_xpath("//*[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a").click()
            await ws.send('Like post: ' + url)
async def youtube_auto_unlike(link):
    for i in link:
        browser.get('https://www.youtube.com/watch?v=' + str(i['id']))
        sleep(3)
        browser.find_elements_by_xpath('//*[@class="style-scope ytd-menu-renderer force-icon-button style-text"]')[0].click()

def youtube_auto_search():
    try:
        key_search = "Elonmust"
        browser.find_element_by_xpath('//*[@id="search-form"]').click()
        sleep(1)
        search = browser.find_element_by_xpath('//*[@aria-label="Search"]')
        search.send_keys(key_search)
        sleep(1)
        search.send_keys(Keys.ENTER)
    except:
        pass
async def listen():
    ws_connect = websockets.connect('ws://127.0.0.1:9097', ping_interval=None)
    async with ws_connect as wb:
        while True:
                param = await wb.recv()

                if "Password" in param:
                    data = json.loads(param)
                    print(type(data))
                    tk = data['Username']
                    mk = data['Password']
                    asyncio.create_task(login(tk,mk))

                if "Posts" in param:
                    print(1)
                    data = json.loads(param)
                    content = data['Posts']['content']
                    media = data['Posts']['media']
                    await asyncio.sleep(10)
                    asyncio.create_task(youtube_auto_post(media, content))

                if "comment" in param:
                    print(1)
                    data = json.loads(param)
                    content = data['comment']['content']
                    link = data['comment']['link']
                    await asyncio.sleep(10)
                    asyncio.create_task(youtube_auto_comment(link, content))
                if "Subcriber" in param:
                    data = json.loads(param)
                    print(1)
                    link = data['Subcriber']['linkSub']
                    await asyncio.sleep(10)
                    asyncio.create_task(youtube_auto_subscribe(link))
                if "Unsubcriber" in param:
                    data = json.loads(param)
                    print(1)
                    await asyncio.sleep(10)
                    link = data['Unsubcriber']['linkunsub']
                    asyncio.create_task(youtube_auto_unsubscribe(link))
                if "Likelink" in param:
                    data = json.loads(param)
                    print(1)
                    await asyncio.sleep(10)
                    link = data['Likelink']['link']
                    asyncio.create_task(youtube_auto_like(link))
                if "unlike" in param:
                    data = json.loads(param)
                    print(1)
                    await asyncio.sleep(10)
                    link = data['unlike']['link']
                    asyncio.create_task(youtube_auto_unlike(link))

                if 'Stop' in param:
                    browser.quit()
                    sys.exit()
async def main():
    task_1 = asyncio.create_task(listen())
    await task_1

if __name__ == '__main__':
    asyncio.run(main())