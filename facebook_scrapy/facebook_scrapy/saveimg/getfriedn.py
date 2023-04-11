import asyncio
import json
import sys

import pandas as pd
import websockets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import numpy as np
import random
import scrapy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



# options = webdriver.chromeOptions()
# prefs = {"profile.default_content_setting_values.notifications" : 2}
# options.add_experimental_option("prefs",prefs)
# options.add_argument("start-maximized")
# browser = webdriver.Edge('E:\Source\msedgedriver.exe', options=options)
options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Edge(executable_path=r'/msedgedriver.exe', options=options)


def wait():
    return sleep(random.randint(5, 8))


browser.get("https://www.facebook.com/")
sleep(3)
# login to facebook
id = browser.find_element_by_xpath('//*[@id="email"]')
id.send_keys("zetabase3i@gmail.com")
pwd = browser.find_element_by_xpath('//*[@id="pass"]')
pwd.send_keys("Giacngo79")
pwd.send_keys(Keys.ENTER)
sleep(3)




def get_friend():

    browser.find_element_by_xpath(
        '//*[@class="bp9cbjyn j83agx80 datstx6m taijpn5t oi9244e8 d74ut37n dt6l4hlj aferqb4h q5xnexhs"]').click()
    sleep(3)
    dem = 0
    while dem < 3:
        print('a')
        browser.find_element_by_xpath('//body').send_keys(Keys.END)
        sleep(1)
        dem += 1

    wait = WebDriverWait(browser, 10)
    wait.until(ec.visibility_of_element_located((By.LINK_TEXT, 'Xem tất cả bạn bè'))).click()
    sleep(5)

    while dem < 10:
        print('a')
        browser.find_element_by_xpath('//body').send_keys(Keys.END)
        sleep(1)
        dem += 1

    page_source = browser.page_source
    soup = bs(page_source, 'lxml')
    friend_local = soup.find('div', class_="j83agx80 btwxx1t3 lhclo0ds i1fnvgqd")
    friend_lst = friend_local.find_all('div',
                                       class_="bp9cbjyn ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi n1f8r23x rq0escxv "
                                              "j83agx80 bi6gxh9e discj3wi hv4rvrfc ihqw7lf3 dati1w0a gfomwglr")
    list_data = []
    for i in friend_lst:
        friend_link = i.find('div', class_="buofh1pr hv4rvrfc")
        # url = friend_link.find('a')['href']
        name = friend_link.find('span',
                                class_="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w "
                                       "c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr "
                                       "lrazzd5p oo9gr5id").text

        print(name)
        data = {
            'id': name,
            'label': name
        }
        list_data.append(data)

    print(list_data)
    print(len(list_data))
    data_string = json.dumps(list_data, indent=4)
    with open('../spiders/FacebookFriend.json', 'w') as f:
        f.write(data_string)

get_friend()

