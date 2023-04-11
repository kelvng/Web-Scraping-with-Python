import asyncio
import json
import sys
import time
from pynput.keyboard import Controller
import websockets
from pywinauto import Application
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
import random


options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument("--profile-directory=Default")
# options.add_argument("--user-data-dir=C:/Users/Admin/AppData/Local/Google/Chrome/User Data")

browser = webdriver.Edge(r'C:\Users\Admin 3i\PycharmProjects\Source\msedgedriver.exe', options=options)

def wait():
    return sleep(random.randint(4,6))



async def login(tk,mk):
    browser.get("https://www.tiktok.com/login/")
    browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[1]/div[2]/div[3]/div[2]').click()
    sleep(2)
    # login to facebook
    print(browser.window_handles)
    browser.switch_to.window(browser.window_handles[1])
    id = browser.find_element_by_xpath('//*[@id="email"]')
    id.send_keys(tk)
    sleep(3)
    pwd = browser.find_element_by_xpath('//*[@id= "pass"]')
    pwd.send_keys(mk)
    sleep(3)
    pwd.send_keys(Keys.ENTER)
    # browser.close()
    browser.switch_to.window(browser.window_handles[0])
    # WebDriverWait(browser, 20).until(EC.invisibility_of_element((By.XPATH, '//*[@data-e2e="upload-icon"]')))
    print(browser.window_handles)
    sleep(15)

#APi https://www.tiktok.com/node/share/video/@beary730/6976969595781434626

async def tiktok_auto_post(content):
    browser.get('https://www.tiktok.com/upload?lang=en')
    print('start Post')
    image_path = r'C:\Users\Public\Video1.mp4'
    sleep(2)
    browser.switch_to.frame(0)


    browser.find_element_by_xpath('//*[@type="file"]').send_keys(image_path)
    sleep(2)
    caption_box = browser.find_element_by_xpath('//*[@class="notranslate public-DraftEditor-content"]')
    caption_box.clear()
    caption_box.send_keys(content)
    WebDriverWait(browser, 100).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class="jsx-2580397738 btn-post"]'))).click()
    WebDriverWait(browser, 100).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@class="jsx-461155393 jsx-3220008684 modal-title"]')))
    print('upload done')
    browser.switch_to.default_content()

async def tiktok_auto_comment(post, content):
    print('comment')
    for i in post:
        browser.get(i)
        sleep(5)
        try:
            page_source = browser.page_source
            soup = bs(page_source, 'lxml')
            links = []
            # tìm tất cả đường link của các group
            # comment 30 baif vieets ddaauf treen mooix page
            page_groups = soup.find("div", {"data-e2e": "user-post-item-list"})
            for s in page_groups.find_all('a'):
                try:
                    link = s['href']
                    if 'video' in link:
                        links.append(link)
                except:
                    pass
            links = list(set(links))
            for link in links:
                print(link)

            print(len(links))
            for link in links:

                browser.get(link)
                sleep(2)
                browser.find_element_by_xpath('//*[@data-e2e="comment-icon"]').click()
                sleep(2)
                try:
                    browser.find_element_by_xpath('//*[@aria-label="Close"]').click()
                    sleep(2)
                except:
                    pass
                browser.find_element_by_xpath('//*[@data-e2e="comment-at-icon"]').click()
                #//*[contains(concat( " ", @class, " " ), concat( " ", "public-DraftStyleDefault-ltr", " " ))]
                comment = browser.find_element_by_xpath('//*[@class="notranslate public-DraftEditor-content"]')
                comment.clear()
                comment.send_keys(content)
                wait()
                browser.find_element_by_xpath('//*[@data-e2e="comment-post"]').click()
                wait()
        except:
            pass
        try:
            sleep(2)
            browser.find_element_by_xpath('//*[@data-e2e="comment-icon"]').click()
            sleep(2)
            try:
                browser.find_element_by_xpath('//*[@aria-label="Close"]').click()
                sleep(2)
            except:
                pass
            browser.find_element_by_xpath('//*[@data-e2e="comment-at-icon"]').click()
            # //*[contains(concat( " ", @class, " " ), concat( " ", "public-DraftStyleDefault-ltr", " " ))]
            comment = browser.find_element_by_xpath('//*[@class="notranslate public-DraftEditor-content"]')
            comment.clear()
            comment.send_keys(content)
            wait()
            browser.find_element_by_xpath('//*[@data-e2e="comment-post"]').click()
            wait()
        except:
            pass

async def tiktok_auto_follow(userlink):
    # products_data = pd.read_csv('..\page_link.csv')
    # WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "profile-icon")))
    for i in userlink:
        browser.get(i)
        wait()
        try:
            sleep(1)
            browser.find_element_by_xpath('//*[@data-e2e="follow-button"]').click()
            sleep(2)
        except:
            pass
async def tiktok_auto_Unfollow(userlink):

    for i in userlink:
        browser.get(i)
        wait()
        try:
            browser.find_element_by_xpath('//*[@class="tiktok-ugux24-DivFollowIconContainer e143oaad6"]').click()
        except:
            wait()
            pass


    sleep(1)
    browser.quit()
async def tiktok_auto_like(like, status):
    for i in like:
        browser.get("https://www.tiktok.com/@hoaa.hanassii?lang=en")
        # kéo tới cuối trang để load tất cả các group nếu status = ALL
        # status # ALL thì quét 30 bài đầu tiên
        try:
            if status == 'ALL':
                reached_page_end = False
                last_height = browser.execute_script("return document.body.scrollHeight")

                while not reached_page_end:
                    browser.find_element_by_xpath('//body').send_keys(Keys.END)
                    await asyncio.sleep(2)
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    if last_height == new_height:
                            reached_page_end = True
                    else:
                            last_height = new_height
            else:
                pass

            sleep(5)
            page_source = browser.page_source
            soup = bs(page_source, 'lxml')

            links = []
            # tìm tất cả đường link của các group
            page_groups = soup.find("div", {"data-e2e":"user-post-item-list"})
            for s in page_groups.find_all('a'):
                try:
                    link = s['href']
                    if 'video' in link :
                        links.append(link)

                except:
                    pass
            links = list(set(links))
            for link in links:
                print(link)

            print(len(links))
            for link in links:
                browser.get(link)
                sleep(2)
                try:
                    browser.find_element_by_xpath('//*[@data-e2e="like-icon"]').click()
                except:
                     pass
        except:
            pass
        sleep(2)
        try:
            browser.find_element_by_xpath('//*[@data-e2e="like-icon"]').click()
        except:
            pass

async def tiktok_auto_unlike(like, status):
    #link có thể là trang cá nhân hoặc là trang video post
    for i in like:
        browser.get(i)
        # kéo tới cuối trang để load tất cả các group nếu status = ALL
        # status # ALL thì quét 30 bài đầu tiên
        try:
            if status == 'ALL':
                reached_page_end = False
                last_height = browser.execute_script("return document.body.scrollHeight")

                while not reached_page_end:
                    browser.find_element_by_xpath('//body').send_keys(Keys.END)
                    await asyncio.sleep(2)
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    if last_height == new_height:
                        reached_page_end = True
                    else:
                        last_height = new_height
            else:
                pass

            sleep(5)
            page_source = browser.page_source
            soup = bs(page_source, 'lxml')

            links = []
            # tìm tất cả đường link của các group
            page_groups = soup.find("div", {"data-e2e": "user-post-item-list"})
            for s in page_groups.find_all('a'):
                try:
                    link = s['href']
                    if 'video' in link:
                        links.append(link)

                except:
                    pass
            links = list(set(links))
            for link in links:
                print(link)

            print(len(links))
            for link in links:
                browser.get(link)
                sleep(2)
                try:
                    browser.find_element_by_xpath('//*[@data-e2e="like-icon"]').click()
                except:
                    pass

        except:
            pass
        sleep(2)
        try:
            browser.find_element_by_xpath('//*[@data-e2e="like-icon"]').click()
        except:
            pass


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True




def tiktok_auto_search():
    sleep(5)
    try:
        key_search = "Elonmust"
        browser.find_element_by_xpath('//*[@placeholder="Search accounts and videos"]').click()
        sleep(1)
        print(1)
        search = browser.find_element_by_xpath('//*[@placeholder="Search accounts and videos"]')
        print(2)
        search.send_keys(key_search)
        sleep(1)
        print(3)
        search.send_keys(Keys.ENTER)
        print(4)

    except:
        pass
    # browser.quit()

async def listen():
    ws_connect = websockets.connect('ws://127.0.0.1:9097', ping_interval=None)
    async with ws_connect as wb:
        while True:
                param = await wb.recv()

                if "Username" in param:
                    data = json.loads(param)
                    print(type(data))
                    tk = data['Username']
                    mk = data['Password']
                    await asyncio.sleep(5)
                    asyncio.create_task(login(tk,mk))

                if "media" in param:
                    data = json.loads(param)
                    content= data["post"]['Content']
                    await asyncio.sleep(5)
                    asyncio.create_task(tiktok_auto_post(content))

                if "comment" in param:
                    data = json.loads(param)
                    link = data['comment']['Post']
                    content = data['comment']['content']
                    await asyncio.sleep(5)
                    asyncio.create_task(tiktok_auto_comment(link, content))
                if "followuser" in param:
                    data = json.loads(param)
                    userlink = data['follow']['userid']
                    await asyncio.sleep(5)
                    asyncio.create_task(tiktok_auto_follow(userlink))
                if "unfollow" in param:
                    data = json.loads(param)
                    userlink = data['unfollow']['userid']
                    await asyncio.sleep(5)
                    asyncio.create_task(tiktok_auto_Unfollow(userlink))
                if "like" in param:
                    data = json.loads(param)
                    userlink = data['like']['Post']
                    status = data['like']['status']
                    await asyncio.sleep(5)
                    asyncio.create_task(tiktok_auto_like(userlink, status))
                if "like" in param:
                    data = json.loads(param)
                    userlink = data['like']['Post']
                    status = data['like']['status']
                    await asyncio.sleep(5)
                    asyncio.create_task(tiktok_auto_unlike(userlink, status))

                # if 'Stop' in param:
                #     # flagstop = True
                #     browser.quit()
                #     sys.exit()
async def main():
    task_1 = asyncio.create_task(listen())
    await task_1

if __name__ == '__main__':
    asyncio.run(main())
