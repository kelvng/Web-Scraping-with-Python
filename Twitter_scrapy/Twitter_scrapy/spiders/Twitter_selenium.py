# coding=utf8
# -*- coding: utf-8 -*-
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
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\msedgedriver.exe', options=options)
URL ="ws://127.0.0.1:9097"
def wait():
    return sleep(random.randint(2,4))

async def login(tk,mk,name):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Currently logged with User: ' +name)
        browser.get("https://twitter.com/i/flow/login")
        wait()
        id = browser.find_element_by_xpath('//*[@autocomplete="username"]')
        id.send_keys(tk)
        wait()
        browser.find_element_by_xpath('//*[@style="color: rgb(255, 255, 255);"]').click()
        wait()
        try:
            pwd = browser.find_element_by_xpath('//*[@name="text"]')
            pwd.send_keys(name)
        except:
            pass
        browser.find_element_by_xpath('//*[@style="color: rgb(255, 255, 255);"]').click()
        wait()
        pwd = browser.find_element_by_xpath('//*[@name="password"]')
        pwd.send_keys(mk)
        browser.find_element_by_xpath('//*[@data-testid="LoginForm_Login_Button"]').click()
        wait()
        await ws.send('Login Success!')
        sleep(6)

async def twitter_auto_post(content, friend, media):
    browser.get('https://twitter.com/')
    sleep(2)
    async with websockets.connect(URL, ping_interval=None) as ws:
        browser.find_element_by_xpath('//*[@data-testid="tweetTextarea_0"]').click()
        sleep(2)
        comment_box = browser.find_element_by_xpath('//*[@data-testid="tweetTextarea_0"]')
        comment_box.send_keys(content +  '@' +friend + media)
        wait()
        browser.find_element_by_xpath('//*[@data-testid="tweetButtonInline"]').click()
        await ws.send("Posted!" + '\n' + "Content: " + content + '\n'+ '@'+friend +'\n' + media)

async def twitter_auto_follow(ID):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Follow!')
        for i in range(len(ID)):
            browser.get('https://twitter.com/' + str(ID[i]))
            await ws.send('Following: ' + str(ID[i]))
            wait()
            try:
                browser.find_element_by_xpath('//*[@style="background-color: rgb(15, 20, 25);"]').click()
            except:
                pass
async def twitter_auto_unfollow(ID):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Unfollowing!')
        for i in range(len(ID)):
            browser.get('https://twitter.com/' + str(ID[i]))
            wait()
            await ws.send('Unfollowing: ' + str(ID[i]))
            try:
                browser.find_element_by_xpath('//*[@class="css-18t94o4 css-1dbjc4n r-1niwhzg r-sdzlij r-1phboty r-rs99b7 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr"]').click()
                wait()
                browser.find_element_by_xpath('//*[@data-testid="confirmationSheetConfirm"]').click()
            except:
                pass


async def twitter_auto_like(linkpost):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Like!')
        for i in range(len(linkpost)):
            browser.get(linkpost[i])
            await ws.send('Like post: ' + linkpost[i])
            try:
                await asyncio.sleep(2)
                wait()
                browser.find_element_by_xpath('//*[@aria-label="Like"]').click()
            except:
                wait()

async def twitter_auto_unlike(linkpost):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Unlike!')
        for i in range(len(linkpost)):
            browser.get(linkpost[i])
            await ws.send('Unlike: ' + linkpost[i])
            try:
                wait()
                browser.find_element_by_xpath('//*[@aria-label="Liked"]').click()
            except:
                wait()

def reply_tweet_comment():
    tweet_link = 'https://twitter.com/NigmaGalaxy/status/1513803931310252037?s=20&t=GmNEa222VilhHGvIiI28Lw'
    browser.get(tweet_link)
    pass

async def twitter_auto_comment(linkpost,content, friend):
    async with websockets.connect(URL, ping_interval=None) as ws:
        await ws.send('Start Comment!')
        #lấy post link trong file
        for i in range(len(linkpost)):
            browser.get(linkpost[i])
            sleep(3)
            browser.find_element_by_xpath('//*[@aria-label="Reply"]').click()
            sleep(2)
            comment_box = browser.find_element_by_xpath('//*[@data-testid="tweetTextarea_0"]')
            await ws.send('Comment post: ' + linkpost[i])
            sleep(1)
            comment_box.send_keys(content + '@' +friend)
            sleep(1)
            browser.find_element_by_xpath('//*[@class="css-1dbjc4n r-1p0dtai r-1d2f490 r-1xcajam r-zchlnj r-ipm5af"]').click()
            # comment_box.click()
            sleep(3)
            browser.find_element_by_xpath('//*[@data-testid="tweetButton"]').click()
            print(3)
            await ws.send('Content: ' + content + '\n' + '@' + friend)
            sleep(1)




async def init_post(content, friend, media):
    print("Post")
    await asyncio.sleep(5)
    asyncio.create_task(twitter_auto_post(content, friend, media))

async def init_follow(ID):
    print("follow")
    await asyncio.sleep(5)
    asyncio.create_task(twitter_auto_follow(ID))
async def init_unfollow(ID):
    print("unfollow")
    await asyncio.sleep(5)
    asyncio.create_task(twitter_auto_unfollow(ID))
async def init_like(linkpost):
    print("like")
    await asyncio.sleep(5)
    asyncio.create_task(twitter_auto_like(linkpost))
async def init_unlike(linkpost):
    print("unlike")
    await asyncio.sleep(5)
    asyncio.create_task(twitter_auto_unlike(linkpost))
async def init_comment(linkpost,content,friend):
    print("comment")
    await asyncio.sleep(5)
    asyncio.create_task(twitter_auto_comment(linkpost,content, friend))

async def listen():
    ws_connect = websockets.connect('ws://127.0.0.1:9097', ping_interval=None)
    async with ws_connect as wb:
        while True:
            param = await wb.recv()
            print(param)
            if "UserName" in param:
                data = json.loads(param)
                print(type(data))
                tk = data['UserName']
                mk = data['PassWord']
                name = data['Description']
                asyncio.create_task(login(tk, mk,name))

            if "Main_post" in param:
                data = json.loads(param)
                content = data['Start post content']['Main_post']['Content']
                friend = data['Start post content']['Main_post']['Hashtag']
                media = data['Start post content']['Main_post']['media']
                asyncio.create_task(init_post(content, friend, media))
            if "Comment_post" in param:
                data = json.loads(param)
                linkpost = data['Comment_post']['linkpost']
                content = data['Comment_post']['Content']
                friend = data['Comment_post']['friend']
                asyncio.create_task(init_comment(linkpost,content,friend))

            if "Follow" in param:
                data = json.loads(param)
                id = data['Follow']['ID']
                asyncio.create_task(init_follow(id))
            if "Unfollow" in param:
                data = json.loads(param)
                id = data['Unfollow']['ID']
                asyncio.create_task(init_unfollow(id))
            if "Unfollow" in param:
                data = json.loads(param)
                id = data['Unfollow']['ID']
                asyncio.create_task(init_unfollow(id))
            if "like" in param:
                data = json.loads(param)
                link = data['like']['linkpost']
                asyncio.create_task(init_like(link))
            if "Unlike" in param:
                data = json.loads(param)
                link = data['Unlike']['linkpost']
                asyncio.create_task(init_unlike(link))

            if 'Stop' in param:
                sys.exit()


async def main():
    task_1 = asyncio.create_task(listen())
    await task_1

if __name__ == '__main__':
    asyncio.run(main())
