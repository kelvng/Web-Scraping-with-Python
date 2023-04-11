import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import numpy as np
import random

from tqdm import tqdm

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

# constants
from selenium.webdriver.common import action_chains
import random
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome('E:\Source\chromedriver97.exe', options=options)

def wait():
    return sleep(random.randint(4,6))


browser.get("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
wait()

# login to facebook
id = browser.find_element_by_xpath('//*[@autocomplete="username"]')
id.send_keys("bot3i12345@gmail.com")
sleep(2)
browser.find_element_by_xpath('//*[@id="identifierNext"]').click()
sleep(2)
pwd = browser.find_element_by_xpath('//*[@autocomplete="current-password"]')
pwd.send_keys("bot3i12345@1234")
sleep(1)
browser.find_element_by_xpath('//*[@jsname="LgbsSe"]').click()
sleep(2)

        # to clean popups after login
try:
    browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
except NoSuchElementException:
    print("no save Info")
try:
    browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
except NoSuchElementException:
    print("no notification box")

        # Lấy link bài viết từ file csv
products_data = pd.read_csv('E:\Source\Youtube_scrapy\Youtube_scrapy\Link_Video.csv')
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


