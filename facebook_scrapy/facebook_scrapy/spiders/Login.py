# coding=utf8
# -*- coding: utf-8 -*-
import asyncio
import json
import random
import re
import sys
from datetime import datetime
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
import websockets
from bs4 import BeautifulSoup
from docx import Document
from facebook_scraper import get_group_info
from facebook_scraper import get_posts
from facebook_scraper import get_profile
from facebook_scraper import get_reactors
from pynput.keyboard import Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from pprint import pprint
from facebook_scraper import _scraper, get_page_info
import scrapy

# for post in get_posts('nintendo', pages=4):
#     print(post['text'][:50])

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome(executable_path=r'H:\PycharmProjects\Source\chromedriver.exe',
                           options=options)

cookie = "sb=oKmmY8v-ThCYm0TBur6fHErR; datr=oammY-WLGSV9rb93qsZEp_Mo; dpr=0.8999999761581421; c_user=100073734591574; usida=eyJ2ZXIiOjEsImlkIjoiQXJxeGJ6ODkzOGQ2bSIsInRpbWUiOjE2Nzc4MTE5NDB9; xs=42%3A12g1I23B-ULBEg%3A2%3A1677743426%3A-1%3A6279%3A%3AAcXxwltmEU5LPH7FwnA-2cZRTaONH3UP79lfSVhvWj4; fr=0EngtXMC9jkjdMfA2.AWU05eyPcMMfGITu3Nr2UWcn_Ww.BkAalr.oZ.AAA.0.0.BkAalr.AWX0bSxQrsQ; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1677830562156%2C%22v%22%3A1%7D; wd=2133x481"
def loginFacebookByCookie(cookie):

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
        print(cookie)
        if (cookie != None):
            script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; ");' \
                     ' console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0];' \
                     ' var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000));' \
                     ' var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } }' \
                     ' function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); }' \
                     ' return str; } setCookie("' + cookie + '"); location.href = "https://facebook.com"; })();'


            #script1 = ' javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("{c_user=100073734591574; xs=42%3AGfemPI2zWBeNMw%3A2%3A1677121112%3A-1%3A6279%3A%3AAcWM56DE-oBzs7y1Lgy6Fuc6LkBog938Wvw5dgBjSQ;}"); location.href = "https://facebook.com"; })();'
            browser.execute_script(script)

            sleep(5)
            print(script)
    except:
        print("Error login")
    sleep(5)
    print("End")
name = ['hội doanh nghiệp đà nẵng']
def Crawl_Like():
    #_scraper.login('zetabase3i@gmail.com','Langnghiem04041979')
    #pprint(get_page_info(identifier))
    'https://www.facebook.com/groups/174764463261090/posts/1423663308371193/'
    data1 = get_reactors(post_id='1423663308371193',
                                      set_cookies=r'H:\PycharmProjects\Source\facebook_scrapy\facebook_scrapy\spiders\cookie.json')
    print(type(data1))
    data = pd.DataFrame.from_dict(data1)
    print(data)
    # data2 = get_profile("DirVDrey", cookie=r'H:\PycharmProjects\Source\facebook_scrapy\facebook_scrapy\spiders\cookie.json')
    # print(data2)
    # data3 = get_profile("Trogg.Vii.9", cookie=r'H:\PycharmProjects\Source\facebook_scrapy\facebook_scrapy\spiders\cookie.json')
    # print(data3)
    # data4 = get_group_info("174764463261090")
    # print(data4)


    Postextract = get_posts(group='174764463261090',
                     cookie=r'H:\PycharmProjects\Source\facebook_scrapy\facebook_scrapy\spiders\cookie.json',
                     pages=2)

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
        like = data['likes'][a]
        comment = data['comments'][a]
        share = data['shares'][a]

        print(time_post)
        print(User)
        print(time_post)
        print(React)
        print(user_id)
        print(posturl)
        a = a+1

    pass
#loginFacebookByCookie(cookie)
#Crawl_Like()
group = ['dota2cvn']
def listen_content(group,datenow, endtime):
    currenttime = datenow
    for i in group:
        groupid = i
        Postextract = get_posts(group=groupid,
                                cookie=r'H:\PycharmProjects\Source\facebook_scrapy\facebook_scrapy\spiders\cookie1.json',
                                pages=1,
                                credentials=("nguyenvanhuy10a3@gmail.com","M@rcilord1047"))

        data = pd.DataFrame.from_dict(Postextract)
        data.to_csv(r'H:\PycharmProjects\Source\facebook_scrapy\facebook_scrapy\spiders\Fb_page.csv')
        a = 0
        print(data)
        while a < len(data):
            time_post = data['time'][a]
            content1 = data['text'][a]
            User = data['username'][a]
            React = data['reactors'][a]
            user_id = data['user_id'][a]
            posturl = data['post_url'][a]
            like = data['likes'][a]
            comment = data['comments'][a]
            share = data['shares'][a]
            #print(time_post)
            if check_time(endtime, time_post) == 1:
                print("--------------------!!!!!!----------------------------------------------")
                print("user Post: "+User)
                print("User Id: "+str(user_id))
                print("Time Post: " + str(time_post))
                #print(content1)
                print("Post Url: "+ posturl)
                print("Like Count: "+str(like))
                print("Count CMT: "+str(comment))
                print("Count Share: "+str(share))
                User_Info = get_profile(user_id,
                                    cookie=r'H:\PycharmProjects\Source\facebook_scrapy\facebook_scrapy\spiders\cookie.json')
                print("User Info"+ str(User_Info))
            else:
                print('false')

            a = a + 1
        print("NewSeasion")
        EndTime = datenow.now()

    pass
EndTime =datetime.now()
def check_time(from_time, time_post):
    from_time1 = from_time.strftime("%Y-%m-%d")
    if datetime.strptime(str(time_post), "%Y-%m-%d %H:%M:%S") > datetime.strptime(str(from_time1), "%Y-%m-%d") :
        return 1
    else:
        return 0
def check():
    print("Hello")

def run(condition):
    # while datetime.now().minute not in {0, 15, 30,
    #                                     45}:  # Wait 1 second until we are synced up with the 'every 15 minutes' clock
    #     sleep(1)
    def task():
        check()
        listen_content(group,datetime.now(),EndTime)
    task()

    while condition == True:
        sleep(60 * 3)  # Wait for 15 minutes
        task()
#run(True)

def Get_Reactor():
    idpost ='2903019553164555'
    browser.get('https://facebook.com/' + idpost)
    sleep(2)
    browser.find_element(By.XPATH,'//span[@class="xt0b8zv x1jx94hy xrbpyxo xl423tq"]').click()
    # scrollable_popup = browser.find_element(By.XPATH, '//*[@id="mount_0_0_cZ"]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div')
    # for i in range(5):
    #     browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_popup)
    #     browser.sleep(2)
    sleep(5)
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    profileurls = soup.find_all('span',class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')
    for i in profileurls:
        profileurl = i.find('a')['href']
        print(profileurl)



    pass
loginFacebookByCookie(cookie)
Get_Reactor()

