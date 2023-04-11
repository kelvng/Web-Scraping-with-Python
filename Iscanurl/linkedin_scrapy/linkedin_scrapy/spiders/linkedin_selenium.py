import asyncio
import json
import pathlib
import re
import sys
from datetime import datetime
import csv
import pandas as pd
import requests
from docx import Document
from facebook_scraper import get_posts
from pynput.keyboard import Key, Controller
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import random
import websockets
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
#options.add_argument('disable_infobars')
options.add_argument("start-maximized")
#options.add_argument('--headless')
browser = webdriver.Edge(executable_path=r'E:\PycharmProjects\Source\msedgedriver100.exe', options=options)






async def login(tk, mk):
    browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    user = browser.find_element_by_xpath('//*[@name="session_key"]')
    user.send_keys(tk)
    sleep(2)
    pwd = browser.find_element_by_xpath('//*[@name="session_password"]')
    pwd.send_keys(mk)
    sleep(2)
    browser.find_element_by_xpath('//*[@type="submit"]').click()

async def linkedin_auto_post(content, hashtag, media):

    browser.find_element_by_xpath('//*[@class="artdeco-button artdeco-button--muted artdeco-button--4 artdeco-button--tertiary ember-view share-box-feed-entry__trigger"]').click()
    sleep(2)
    text_box = browser.find_element_by_xpath('//*[@aria-label="Text editor for creating content"]')
    text_box.send_keys(content + '\n' + hashtag + '\n' + media)

    sleep(2)
    browser.find_element_by_xpath('//*[@class="share-box_actions"]').click()
    sleep(2)


def linkedin_comment(post, content):
    for i in range(len(post)):
        browser.get(post[i])
        sleep(2)
        text_box = browser.find_element_by_xpath('//*[@aria-placeholder="Add a comment…"]')
        text_box.send_keys(content)
        sleep(2)
        browser.find_element_by_xpath('//*[@class="comments-comment-box__submit-button mt3 artdeco-button artdeco-button--1 artdeco-button--primary ember-view"]').click()
        sleep(2)

async def linkedin_get_content(post):
    content = []
    for i in range(len(post)):
        browser.get(post[i])
        content.append(post[i])
        sleep(2)
        data = browser.find_element_by_xpath('//*[@class="feed-shared-update-v2__description-wrapper"]')
        text = data.text
        content.append(text)
        img = browser.find_element_by_xpath('//*[@class="ivm-view-attr__img--centered feed-shared-image__image feed-shared-image__image--constrained lazy-image ember-view"]').get_attribute("src")
        print(img)
    print(content)

    pass

async def linkedin_like(post):
    for i in range(len(post)):
        browser.get(post[i])
        sleep(2)
        browser.find_element_by_xpath('//*[@type="like-icon"]').click()
        sleep(2)
async def linkedin_unlike(post):
    for i in range(len(post)):
        browser.get(post[i])
        sleep(2)
        browser.find_element_by_xpath('//*[@class="reactions-react-button feed-shared-social-action-bar__action-button"]').click()
        sleep(2)


profile = ['https://www.linkedin.com/in/linhthaiofficial/', 'https://www.linkedin.com/in/jehakjerrylee/']

async def listen():
    ws_connect = websockets.connect('ws://127.0.0.1:9097', ping_interval=None)
    async with ws_connect as wb:
        while True:
            param = await wb.recv()
            data = json.loads(param)
            print(data)
            if 'PassWord' in param:
                data = json.loads(param)
                tk = data['UserName']
                mk = data['PassWord']
                asyncio.create_task(login(tk, mk))
            if 'Start post content' in param:
                content = data['Start post content']['content']['content']
                media = data['Start post content']['content']['Image']
                hashtag = "data['Post']['Main_post']['hashtag']"
                asyncio.create_task(linkedin_auto_post(content, hashtag, media))
            if 'Get' in param:
                post =data['Get']['post']
                asyncio.create_task(linkedin_get_content(post))
            if 'Like' in param:
                post = data['Like']['post']
                asyncio.create_task(linkedin_like(post))
            if 'Unlike' in param:
                post = data['Unlike']['post']
                asyncio.create_task(linkedin_unlike(post))
                #login()

async def main():
    task_1 = asyncio.create_task(listen())
    await task_1

if __name__ == '__main__':
    asyncio.run(main())
