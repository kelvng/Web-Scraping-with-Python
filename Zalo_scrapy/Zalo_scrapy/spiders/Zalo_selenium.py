import urllib.request

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
from bs4 import BeautifulSoup
import random
from azcaptchaapi import AZCaptchaApi
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm





options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome(r'C:\Users\Admin 3i\PycharmProjects\Source\chromedriver.exe', options=options)

def wait():
    return sleep(random.randint(5,8))

# API key của bên giải quyết captcha
API_KEY = 'lzqixvjq2byp9zuxahp5dkwfnf1jsy8v'

api = AZCaptchaApi(API_KEY)

def login(tk,mk):
    browser.get("https://chat.zalo.me/")
    wait()
    browser.find_element_by_xpath('//*[@class="body"]/div[2]/div/ul/li[2]').click()
    # login to
    id = browser.find_element_by_xpath('//*[@placeholder="Số điện thoại"]')
    id.send_keys(tk)
    sleep(2)
    pwd = browser.find_element_by_xpath('//*[@placeholder="Mật khẩu"]')
    pwd.send_keys(mk)
    sleep(2)
    pwd.send_keys(Keys.ENTER)

    captcha = True
    while captcha:
        # print("get page source")
        page_source = browser.page_source

        # print("find captcha image")
        soup = BeautifulSoup(page_source, 'lxml')

        links_captcha_img = soup.find("div", class_="z_64zMZRh7__2055")['src']
        # có trường hợp bắt không được link hình ảnh, nên sẽ sử dụng hình ảnh cũ để cố tình nhập sai cho website nhả link hình captcha mới
        try:
            img = urllib.request.urlretrieve(links_captcha_img, '../../../captcha.png')[0]
        except ValueError:
            img = 'captcha.png'
        # print('captcha img downloaded')

        captcha = api.solve(img)

        # print('\nTry to get captcha answer')
        result = captcha.await_result()
        # print('\nGot answer: ' + result)
        result_captcha_box = WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[5]/div/div[1]/div[1]/div/div/span[1]/form/div/ul/li[1]/input')))
        result_captcha_box.clear()
        result_captcha_box.send_keys(result)
        result_captcha_box.send_keys(Keys.ENTER)
        #count_pass_captcha += 1
        try:
            WebDriverWait(browser, 3).until(EC.alert_is_present())
            alert = browser.switch_to.alert
            alert.accept()
            # print("\nwrong captcha")
            # áp dụng delay tránh trường hợp code chạy nhanh hơn quá trình reload hình ảnh captcha
            sleep(3)

        except TimeoutException:
            captcha = False

login('0934479119', 'Langnghiem79')

#facebook_auto_post_group
