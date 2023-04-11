import asyncio
import json
import os
import sys
from telnetlib import EC

import pandas as pd
import websockets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import numpy as np
import random
from pywinauto.application import Application

from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

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
driver_path = r'E:\PycharmProjects\Source\msedgedriver100.exe'
browser = webdriver.Chrome(executable_path=driver_path, options=options)

def wait():
    return sleep(random.randint(4,6))


browser.get("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
async def login(tk,mk):
# login to facebook
    id = browser.find_element_by_xpath('//*[@autocomplete="username"]')
    id.send_keys(tk)
    sleep(1)
    browser.find_element_by_xpath('//*[@id="identifierNext"]').click()
    sleep(1)
    pwd = browser.find_element_by_xpath('//*[@autocomplete="current-password"]')
    pwd.send_keys(mk)
    sleep(1)
    browser.find_element_by_xpath('//*[@jsname="LgbsSe"]').click()


        # to clean popups after login

def youtube_auto_comment():
        products_data = pd.read_csv('E:\Source\Youtube_scrapy\Youtube_scrapy\Link_Video.csv')
        for product in tqdm(products_data['Link'].tolist()):
            browser.get(product)
            sleep(5)
            browser.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            sleep(5)
            browser.find_element_by_xpath('//*[@id="placeholder-area"]').click()
            sleep(2)
            item = browser.find_element_by_xpath('//*[@id="contenteditable-root"]')
            comment = "I like it!\n This is the most amazing things ever seen.\n Wanna see more~\n"
            item.send_keys(comment)
            item.send_keys(Keys.CONTROL, Keys.ENTER)

            wait()
            browser.quit()
async def youtube_auto_subscribe():
    name= 'yt remix'
    search = browser.find_element_by_xpath('//*[@name="search_query"]')
    search.send_keys(name)
    search.send_keys(Keys.CONTROL, Keys.ENTER)
    await asyncio.sleep(2)
    browser.find_element_by_xpath("//yt-formatted-string[text()='Subscribe']").click()

    #browser.quit()
def youtube_auto_unsubscribe():
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no save Info")
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no notification box")

            # Lấy link bài viết từ file csv
    products_data = pd.read_csv('..\Link_Video.csv')
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
                # tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual

        sleep(3)
        browser.find_element_by_xpath('//*[@class="style-scope ytd-subscribe-button-renderer"]').click()
        try:
            sleep(1)
            browser.find_element_by_xpath('//*[@aria-label="Unsubscribe"]').click()
        except:
            wait()

                # finally:
                # browser.find_element_by_xpath('//*[@aria-label="Gỡ Thích"]').click()
                # wait()
    sleep(2)
    browser.quit()
def youtube_auto_like():
    video = [{'id':'CK6K1EjsJAk'}]
    for i in range(len(video)):
        browser.get('https://www.youtube.com/watch?v='+video[i]['id'])
        sleep(3)
        browser.find_element_by_xpath("//*[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a").click()
        try:
            sleep(1)
            comment_box = browser.find_element_by_xpath('//*[@aria-label="Tweet text"]')
            sleep(2)
            comment_box.send_keys("Good")
            wait()
            browser.find_element_by_xpath('//*[@data-testid="tweetButton"]').click()
            wait()
        except:
            wait()

                # finally:
                # browser.find_element_by_xpath('//*[@aria-label="Gỡ Thích"]').click()
                # wait()
    sleep(1)
    browser.quit()
    sys.exit()
def youtube_auto_unlike():
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no save Info")
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no notification box")

            # Lấy link bài viết từ file csv
    products_data = pd.read_csv('..\Link_Video.csv')
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
                # tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual

        sleep(3)
        browser.find_element_by_xpath("//*[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a").click()
        try:
            sleep(1)
            comment_box = browser.find_element_by_xpath('//*[@aria-label="Tweet text"]')
            sleep(2)
            comment_box.send_keys("Good")
            wait()
            browser.find_element_by_xpath('//*[@data-testid="tweetButton"]').click()
            wait()
        except:
            wait()

                # finally:
                # browser.find_element_by_xpath('//*[@aria-label="Gỡ Thích"]').click()
                # wait()
    sleep(1)
    browser.quit()
async def youtube_auto_post(content):
    filepath = 'E:\PycharmProjects\Source\Youtube_scrapy\Youtube_scrapy\spiders\Video1.mp4'
    # if title is not in data, return immediately
    # navigate to the upload page
    browser.get('https://studio.youtube.com/')
    # click on 'Create' button
    browser.find_element_by_id('create-icon').click()
    await asyncio.sleep(1)
    # Click on 'Upload Video'
    browser.find_element_by_xpath('//*[@test-id="upload-beta"]').click()

    await asyncio.sleep(1)

    browser.find_element_by_xpath(
        '//div[contains(text(), "Select files")]').click()
    # Get Input Element
    # Title
    await asyncio.sleep(1)
    upload_dialog = Application().connect(title_re='Open')
    upload_dialog.Open.Edit.type_keys(filepath)
    await asyncio.sleep(5)
    upload_dialog.window(title_re='Open').Open.click()
    await asyncio.sleep(3)
    item = browser.find_element_by_xpath('//*[@aria-label="Add a title that describes your video"]')
    item.send_keys(content)
    item.send_keys(Keys.CONTROL, Keys.ENTER)
    browser.find_element_by_xpath('//*[@name="VIDEO_MADE_FOR_KIDS_MFK"]').click()
    # Next
    browser.find_element_by_id('next-button').click()
    browser.find_element_by_id('next-button').click()
    browser.find_element_by_id('next-button').click()

    visibilities = ['PUBLIC', 'UNLISTED', 'PRIVATE']
    browser.find_element_by_xpath('//*[@name="' + visibilities[0] + '"]').click()
    # Done
    browser.find_element_by_id('done-button').click()
def youtube_auto_search():
    try:
        key_search = "Elonmust"
        browser.find_element_by_xpath('//*[@id="search-form"]').click()
        sleep(1)
        search = browser.find_element_by_xpath('//*[@aria-label="Search"]')
        search.send_keys(key_search)
        sleep(1)
        search.send_keys(Keys.ENTER)

        #browser.quit()
    except:
        pass
async def listen():
    ws_connect = websockets.connect('ws://127.0.0.1:9097', ping_interval=None)
    async with ws_connect as wb:
        while True:
                param = await wb.recv()

                if "UserName" in param:
                    data = json.loads(param)
                    print(type(data))
                    tk = data['UserName']
                    mk = data['PassWord']
                    asyncio.create_task(login(tk,mk))

                if "Post video" in param:
                    print(1)
                    data = json.loads(param)
                    content = data['Post video']['content']['content']
                    await asyncio.sleep(10)
                    asyncio.create_task(youtube_auto_post(content))
                if "Subsribe " in param:
                    print(1)
                    await asyncio.sleep(10)
                    asyncio.create_task(youtube_auto_subscribe())
                if "Like" in param:
                    print(1)
                    await asyncio.sleep(10)
                    asyncio.create_task(youtube_auto_like())

                # if 'Stop' in param:
                #     # flagstop = True
                #     browser.quit()
                #     sys.exit()
async def main():
    task_1 = asyncio.create_task(listen())
    await task_1

if __name__ == '__main__':
    asyncio.run(main())