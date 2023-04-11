import TestScrapy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import numpy as np
import random

from tqdm import tqdm

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome('E:\Source\chromedriver97.exe', options=options)

def wait():
    return sleep(random.randint(5,8))


browser.get("https://www.facebook.com")
wait()

# login to facebook
id = browser.find_element_by_xpath('//*[@id="email"]')
id.send_keys("zetabase3i@gmail.com")
pwd = browser.find_element_by_xpath('//*[@id="pass"]')
pwd.send_keys("Langnghiem@79")
pwd.send_keys(Keys.ENTER)

sleep(3)
products_data = pd.read_csv('E:\Source\group_links.csv')
for link in tqdm(products_data['Link'].tolist()):
    browser.get(link)
    wait()

    links_post = []

    group_id = link.split(".")[-2]

    for post in tqdm(TestScrapy.get_posts(group=group_id, pages=3)):
            if 'permalink' in post['post_url']:
                links_post.append(post['post_url'].replace("m.", ""))

    # save file chứa link post
    links_post = np.array(links_post)
    np.save("post_links.json", links_post)