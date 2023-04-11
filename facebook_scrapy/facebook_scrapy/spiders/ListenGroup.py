# coding=utf8
# -*- coding: utf-8 -*-
import asyncio
import json
import random
import re
import sys
from datetime import datetime
from time import sleep
import pandas as pd
import requests
import websockets
from bs4 import BeautifulSoup
from docx import Document
from facebook_scraper import get_posts
from pynput.keyboard import Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
import scrapy

for post in get_posts('nintendo', pages=1):
    print(post['text'][:50])

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome(executable_path=r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe',
                           options=options)

def wait():
    return sleep(random.randint(5, 8))


start_time = datetime.now()
lstcookie = []
Botresult = []
Botname = []
Botid = []
URL = 'ws://127.0.0.1:9091'
def Bot_func():
    async def loginFacebookByCookie(cookie):
        async with websockets.connect(URL, ping_interval=None) as ws:
            await ws.send('Start Login!')
            try:
                browser.get('https://facebook.com/')
                sleep(1)
            except:
                print("check live fail")
            try:
                new_cookie = ["c_user=", "xs="]
                cookie_arr = cookie.split(";")
                for i in cookie_arr:
                    if i.__contains__('c_user='):
                        new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
                    if i.__contains__('xs='):
                        new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                        if (len(new_cookie[1].split("|"))):
                            new_cookie[1] = new_cookie[1].split("|")[0]
                        if (";" not in new_cookie[1]):
                            new_cookie[1] = new_cookie[1] + ";"
                conv = new_cookie[0] + " " + new_cookie[1]
            except:
                print("Error Convert Cookie")
            try:
                cookie = conv
                #print(cookie)
                if (cookie != None):
                    script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; ");' \
                             ' console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0];' \
                             ' var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000));' \
                             ' var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } }' \
                             ' function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); }' \
                             ' return str; } setCookie("' + cookie + '"); location.href = "https://facebook.com"; })();'

                    # script1 = ' javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("{c_user=100073734591574; xs=42%3AGfemPI2zWBeNMw%3A2%3A1677121112%3A-1%3A6279%3A%3AAcWM56DE-oBzs7y1Lgy6Fuc6LkBog938Wvw5dgBjSQ;}"); location.href = "https://facebook.com"; })();'
                    browser.execute_script(script)
                    await ws.send('Login success!')
                    print('Login success!')
            except:
                print("Error login")
                await ws.send('Login Fail pls check tocken!')
            lstcookie.append(cookie)

    async  def ListenGroup(group):
        Postextract = get_posts(group=group,
                                cookie=r'H:\PycharmProjects\Source\facebook_scrapy\facebook_scrapy\spiders\cookie.json',
                                pages=1)

        data = pd.DataFrame.from_dict(Postextract)
        a = 0
        print(data)
        while a < len(data):
            time_post = data['time'][a]
            content1 = data['text'][a]
            User = data['username'][a]
            React = data['reactors'][a]
            user_id = data['user_id'][a]
            posturl = data['post_url'][a]
            print(time_post)
            print(User)
            print(time_post)
            print(React)
            print(user_id)
            print(posturl)
            a = a + 1
        pass

    def value_to_float(x):
        if type(x) == float or type(x) == int:
            return x
        if 'K' in x:
            if len(x) > 1:
                return float(x.replace('K', '')) * 1000
            return 1000.0
        if 'M' in x:
            if len(x) > 1:
                return float(x.replace('M', '')) * 1000000
            return 1000000.0
        if 'B' in x:
            return float(x.replace('B', '')) * 1000000000
        else:
            return x

    def check_keyword(keyword, content):
        try:
            for x in keyword:
                if x in content:
                    return 1
            return 0
        except:
            pass

    def check_time(from_time, to_time, time_post):
        from_time1 = from_time.replace('T', ' ')
        from_time2 = from_time1.replace('.000Z', '')
        to_time1 = to_time.replace('T', ' ')
        to_time2 = to_time1.replace('.000Z', '')
        if datetime.strptime(str(time_post), "%Y-%m-%d %H:%M:%S") > datetime.strptime(from_time2,
                                                                                      "%Y-%m-%d %H:%M:%S") and datetime.strptime(
            str(time_post), "%Y-%m-%d %H:%M:%S") < datetime.strptime(to_time2, "%Y-%m-%d %H:%M:%S"):
            return 1
        else:
            return 0



    async def listen():
        ws_connect = websockets.connect('ws://127.0.0.1:9091', ping_interval=None)
        async with ws_connect as wb:
            await wb.send('Spider running!')

            while True:

                param = await wb.recv()
                if "UserName" in param:
                    data = json.loads(param)
                    print(type(data))
                    # tk = data['UserName']
                    # mk = data['Password']
                    Botname.append(data['BotSocialName'])
                    Botid.append(data['BotSocialCode'])
                    cookie = data['Cookie']
                    #print(cookie)
                    await asyncio.sleep(5)
                    asyncio.create_task(loginFacebookByCookie(cookie))

                if "Start post content" in param:
                    data = json.loads(param)
                    print(data)
                    linkpost_group1 = data["Start post content"]['Group']
                    #print(linkpost_group1)
                    post_content = data["Start post content"]['content']
                    #print(post_content)
                    await asyncio.sleep(5)
                    asyncio.create_task(facebook_auto_post_group(linkpost_group1, post_content))

                if "Start post comment" in param:
                    data = json.loads(param)
                    await asyncio.sleep(5)
                    group = data["Start post comment"]['Group']
                    content = data["Start post comment"]['content']
                    # friend = data["Start post comment"]['friends']
                    keyword = data["Start post comment"]['keywords']
                    from_time = data["Start post comment"]['from']
                    to_time = data["Start post comment"]['to']
                    asyncio.create_task(facebook_auto_comment(group, content, keyword, from_time, to_time))
                if "Start get content" in param:
                    data = json.loads(param)
                    group = data["Start get content"]['Group']
                    friend = data["Start get content"]['friends']
                    keyword = data["Start get content"]['keywords']
                    from_time = data["Start get content"]['from']
                    to_time = data["Start get content"]['to']
                    await asyncio.sleep(5)
                    asyncio.create_task(get_post_content(group, keyword, from_time, to_time))
                # if "Start get comment" in param:
                #     data = json.loads(param)
                #     group = data['Get']['Comment']['Group']
                #     friend = data['Get']['Comment']['friends']
                #     keyword = data['Get']['Comment']['keywords']
                #     await asyncio.sleep(5)
                #     asyncio.create_task(get_comment_post(friend, keyword))
                # if "Like post" in param:
                #     data = json.loads(param)
                #     print(data)
                #     group = data['Like post']['Group']
                #     friend = data['Like post']['friends']
                #     keyword = data['Like post']['keywords']
                #     from_time = data['Like post']['from']
                #     to_time = data['Like post']['to']
                #     await asyncio.sleep(5)
                #     asyncio.create_task(facebook_auto_like(group, keyword, from_time, to_time))
                # if "Like comment" in param:
                #     group = data['Like']['Comment']['Group']
                #     post = data['Like']['Comment']['post']
                #     friend = data['Like']['Comment']['friends']
                #     keyword = data['Like']['Comment']['keywords']
                #     from_time = data['Like']['Comment']['from']
                #     to_time = data['Like']['Comment']['to']
                #     await asyncio.sleep(5)
                #     asyncio.create_task(facebook_auto_like(group, keyword, from_time, to_time))
                # if "Unlike" in param:
                #     if "Unlike post" in param:
                #         data = json.loads(param)
                #         group = data['Unlike post']['Group']
                #         friend = data['Unlike post']['friends']
                #         keyword = data['Unlike post']['keywords']
                #         from_time = data['Unlike post']['from']
                #         to_time = data['Unlike post']['to']
                #         await asyncio.sleep(5)
                #         asyncio.create_task(facebook_auto_unlike(group, keyword, from_time, to_time))
                #     if "Unlike comment" in param:
                #         group = data['Unlike']['Comment']['Group']
                #         post = data['Unlike']['Comment']['post']
                #         friend = data['Unlike']['Comment']['friends']
                #         keyword = data['Unlike']['Comment']['keywords']
                #         from_time = data['Unlike']['Comment']['from']
                #         to_time = data['Unlike']['Comment']['to']
                #         await asyncio.sleep(5)
                #         asyncio.create_task(facebook_auto_unlike(group, keyword, from_time, to_time))

                # if "Follow" in param:
                #     data = json.loads(param)
                #     name = data['Follow']['Name']
                #     await asyncio.sleep(5)
                #     asyncio.create_task(facebook_auto_unfollow(name))
                # if "Unfollow" in param:
                #     data = json.loads(param)
                #     name = data['Follow']['Name']
                #     await asyncio.sleep(5)
                #     asyncio.create_task(facebook_auto_unfollow(name))
                if "SearchGroup" in param:
                    data = json.loads(param)
                    name = data['SearchGroup']['Name']
                    asyncio.create_task(facebook_auto_search_group(name))
                if "JoinGroup" in param:
                    data = json.loads(param)
                    Group = data['JoinGroup']['Group']
                    asyncio.create_task(facebook_auto_join_group(Group))
                # if "Invite" in param:
                #     data = json.loads(param)
                #     print(data)
                #     group = data['Invite']['Group']
                #     friend = data['Invite']['friends']
                #     page = data['Invite']['page']
                #     await asyncio.sleep(5)
                #     asyncio.create_task(auto_invite(group, page, friend))

                # if "Share post" in param:
                #     data = json.loads(param)
                #     post = data["Share post"]['post']
                #     group = data["Share post"]['group']
                #     page = data["Share post"]['page']
                #     friends = data["Share post"]['friends']
                #     content = data["Share post"]['content']
                #     await asyncio.sleep(5)
                #     asyncio.create_task(fb_share_post(post, friends, group, page, content))
                if "Addfriend" in param:
                    data = json.loads(param)
                    group = data['Addfriend']['Group']
                    asyncio.create_task(add_friend(group))

                if 'Stop' in param:
                    browser.quit()
                    sys.exit()

    async def main():
        task_1 = asyncio.create_task(listen())
        await asyncio.sleep(0.250)
        await task_1


    async def forever():
        while True:
            await main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(forever())

class Myspider(scrapy.Spider):
    name = 'CoreFacebookSpider'
    some_attribute = "Yes|No"
    # http://localhost:9080/crawl.json?spider_name=Tailieu&url=https://tailieu.vn/
    start_urls = ['https://facebook.com/']
    print("hello world !")
    Bot_func()

# if __name__ == '__main__':
#     asyncio.run(main())
