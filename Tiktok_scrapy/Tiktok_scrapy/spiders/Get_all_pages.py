import csv
import json

import csvfile as csvfile
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
import scrapy
from keyboard import press
from selenium.webdriver.common.by import By
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome('C:\\Users\\pycha\\PycharmProjects\\Source\\chromedriver97.exe', options=options)


browser.get("https://www.tiktok.com/login/phone-or-email/email")
WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.NAME, "username"))
)
# login to facebook
id = browser.find_element(By.XPATH,'//*[@name="username"]')
id.send_keys("zetabase3i@gmail.com")
sleep(5)
pwd = browser.find_element(By.XPATH,'//*[@type="password"]')
pwd.send_keys("Langnghiem@040479@79")
sleep(2)
browser.find_element(By.XPATH,'//*[@type="submit"]').click()

sleep(40)



sleep(5)

    # chuyển đường dẫn tới trang nhóm của bản thân
groups_page = browser.current_url + '&sk=groups'

browser.get(groups_page)

sleep(5)

    # kéo tới cuối trang để load tất cả các group



browser.find_element_by_xpath('//body').send_keys(Keys.END)
sleep(2)



sleep(5)

    # lấy content của web rồi pass qua beatifulsoup
page_source = browser.page_source
soup = bs(page_source, 'lxml')

links = []

    # tìm tất cả đường link của các group
page_groups = soup.find("div", {"data-pagelet":"ProfileAppSection_0"})
for s in page_groups.find_all('a'):
        try:
            link = s['href']
           # members = s['/html/body/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/span/div/div[3]/a']
            if 'groups' in link and 'profile.php' not in link:
                links.append(link)
               # links.append(members)
        except:
            pass

links = list(set(links))
for link in links:
        print(link)

print(len(links))

    # export qua file npy hoặc có thể sử dụng định dạng khác nếu muốn
#save_links = csv.writer(links,csvfile, dialect='unix')
#np.save('E:\Source\kqxs\kqxs\group.csv', save_links)
#with open('groups.csv', 'w', newline='links')as csvfile:
    #writer = csv.writer(csvfile, dialect='unix')

Array=np.array(links)
person_dict=json.dumps(links)
with open('kqxs/kqxs/spiders/groups.csv', 'w')as json_file:
    json.dump(person_dict, json_file, default=str, indent=1)