import asyncio
import json
import sys
import time

import websockets
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
browser = webdriver.Edge(r'E:\PycharmProjects\Source\msedgedriver100.exe', options=options)

def wait():
    return sleep(random.randint(4,6))


browser.get("https://www.tiktok.com/login/")
async def login(tk,mk):
    browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[1]/div[2]/div[3]/div[2]').click()
    # login to facebook

    browser.switch_to.window(browser.window_handles[1])
    id = browser.find_element_by_xpath('//*[@id="email"]')
    id.send_keys(tk)
    await asyncio.sleep(1)
    pwd = browser.find_element_by_xpath('//*[@id="pass"]')
    pwd.send_keys(mk)
    pwd.send_keys(Keys.ENTER)
    browser.switch_to.window(browser.window_handles[0])


    wait()

# try:
#     element = WebDriverWait(browser ,20).until(
#         EC.presence_of_element_located((By.ID, "profile-icon"))
#     )
# except:
#     wait()
def tiktok_auto_comment():
    browser.get("https://www.tiktok.com/@hoaa.hanassii?lang=en")
    # kéo tới cuối trang để load tất cả các group
    reached_page_end = False
    last_height = browser.execute_script("return document.body.scrollHeight")


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
                comment.send_keys("Good")
                wait()
                browser.find_element_by_xpath('//*[@data-e2e="comment-post"]').click()
                wait()
    browser.quit()
def tiktok_auto_follow():
    products_data = pd.read_csv('..\page_link.csv')
    # WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "profile-icon")))
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
        wait()
        try:
            sleep(1)
            browser.find_element_by_xpath('//*[@data-e2e="follow-button"]').click()
            sleep(2)
        except:
            wait()


    sleep(1)
    browser.quit()
    wait()
def tiktok_auto_Unfollow():
    products_data = pd.read_csv('..\link.csv')
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
        wait()
        try:
            browser.find_element_by_xpath('//*[@class="tiktok-ugux24-DivFollowIconContainer e143oaad6"]').click()
        except:
            wait()
            pass


    sleep(1)
    browser.quit()
async def tiktok_auto_like():
    browser.get("https://www.tiktok.com/@hoaa.hanassii?lang=en")
    # kéo tới cuối trang để load tất cả các group
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
        try:
            browser.get(link)
            sleep(2)
            try:
                browser.find_element_by_xpath('//*[@data-e2e="like-icon"]').click()
            except:
                 pass
        except:
            pass
        browser.close()
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True
async def tiktok_auto_post():
    await asyncio.sleep(10)
    browser.get('https://www.tiktok.com/upload/?lang=en')
    await asyncio.sleep(5)
    video_path = "E:\PycharmProjects\Source\Tiktok_scrapy\Tiktok_scrapy\spiders\Video1.mp4"
    while True:
        #browser.find_element_by_xpath('//div[contains(text(), "Select video to upload")]').click()
        #browser.find_element_by_xpath('//input[@name='upload-btn']').click()
        #file_uploader = browser.find_element_by_css_selector('.upload-btn-input').click()
        # Input Video
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        browser.switch_to.frame(0)

        file_input_element = browser.find_elements(By.CLASS_NAME, "upload-btn-input")[0]
        file_input_element.send_keys(video_path)

        caption = browser.find_element_by_xpath(
            '//div[2]/div/div/div/div/div/div/div/div')
        browser.implicitly_wait(10)
        ActionChains(browser).move_to_element(caption).click(caption).perform()

        with open(r"E:\PycharmProjects\Source\Tiktok_scrapy\caption.txt", "r") as f:
            tags = [line.strip() for line in f]

        for tag in tags:
            ActionChains(browser).send_keys(tag).perform()
            time.sleep(2)
            ActionChains(browser).send_keys(Keys.RETURN).perform()
            time.sleep(1)

        time.sleep(5)
        browser.execute_script("window.scrollTo(150, 300);")
        time.sleep(5)

        post = WebDriverWait(browser, 100).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@id="root"]/div/div/div/div/div[3]/div[3]/div[8]/button[2]')))
#post buttom
# xpath=//div[@id='root']/div/div/div/div/div[3]/div[3]/div[8]/button[2]
        post.click()
        time.sleep(30)

        if check_exists_by_xpath(browser, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
            reupload = WebDriverWait(browser, 100).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))

            reupload.click()
        else:
            print('Unknown error cooldown')
            while True:
                time.sleep(600)
                post.click()
                time.sleep(15)
                if check_exists_by_xpath(browser, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
                    break

        if check_exists_by_xpath(browser, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
            reupload = WebDriverWait(browser, 100).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))
            reupload.click()

        time.sleep(1)


def tiktok_auto_unlike():
    pass
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

                if "UserName" in param:
                    data = json.loads(param)
                    print(type(data))
                    tk = data['UserName']
                    mk = data['PassWord']
                    asyncio.create_task(login(tk,mk))

                if "Start post content" in param:
                    data = json.loads(param)
                    linkpost_group1 = data["Start post content"]['Group']
                    post_content = data["Start post content"]['content']['content']
                    await asyncio.sleep(6)
                    asyncio.create_task(tiktok_auto_post())

                if "Comment_post" in param:
                    data = json.loads(param)
                    linkcmt_post1 = data['Post']['Comment_post']['Group']
                    comment_content1 = data['Post']['Comment_post']['content']
                    await asyncio.sleep(5)
                    asyncio.create_task(facebook_auto_comment(linkcmt_post1, comment_content1))
                if "Start get content" in param:
                    data = json.loads(param)
                    group = data["Start get content"]['Group']
                    friend = data["Start get content"]['friends']
                    keyword = data["Start get content"]['keywords']
                    from_time = data["Start get content"]['from']
                    to_time = data["Start get content"]['to']
                    await asyncio.sleep(5)
                    asyncio.create_task(get_post_content(group, keyword,friend, from_time, to_time))
                if "Start get comment" in param:
                    data = json.loads(param)
                    group = data['Get']['Comment']['Group']
                    friend = data['Get']['Comment']['friends']
                    keyword = data['Get']['Comment']['keywords']
                    from_time = data['Get']['Comment']['from']
                    to_time = data['Get']['Comment']['to']
                    await asyncio.sleep(5)
                    asyncio.create_task(get_comment_post(group, keyword, from_time, to_time))
                if "Like post" in param:
                    data = json.loads(param)
                    group = data['Like post']['Group']
                    friend = data['Like post']['friends']
                    keyword = data['Like post']['keywords']
                    from_time = data['Like post']['from']
                    to_time = data['Like post']['to']
                    await asyncio.sleep(5)
                    asyncio.create_task(facebook_auto_like(group,  keyword, from_time, to_time))
                if "Like comment" in param:
                    group = data['Like']['Comment']['Group']
                    post = data['Like']['Comment']['post']
                    friend = data['Like']['Comment']['friends']
                    keyword = data['Like']['Comment']['keywords']
                    from_time = data['Like']['Comment']['from']
                    to_time = data['Like']['Comment']['to']
                    await asyncio.sleep(5)
                    asyncio.create_task(facebook_auto_like(group, post, friend, keyword, from_time, to_time))
                if "Unlike" in param:
                    if "Post" in param:
                        data = json.loads(param)
                        group = data['Unlike']['Post']['Group']
                        friend = data['Unlike']['Post']['friends']
                        keyword = data['Unlike']['Post']['keywords']
                        from_time = data['Unlike']['Post']['from']
                        to_time = data['Unlike']['Post']['to']
                        await asyncio.sleep(5)
                        asyncio.create_task(facebook_auto_unlike(group, friend, keyword, from_time, to_time))
                    else:
                        group = data['Unlike']['Comment']['Group']
                        post = data['Unlike']['Comment']['post']
                        friend = data['Unlike']['Comment']['friends']
                        keyword = data['Unlike']['Comment']['keywords']
                        from_time = data['Unlike']['Comment']['from']
                        to_time = data['Unlike']['Comment']['to']
                        await asyncio.sleep(5)
                        asyncio.create_task(facebook_auto_unlike(group, post, friend, keyword, from_time, to_time))
                if "Invite" in param:
                    data = json.loads(param)
                    group = data['Invite']['Group']
                    friend = data['Invite']['friends']
                    page = data['Invite']['page']
                    await asyncio.sleep(5)
                    asyncio.create_task(auto_invite(group,page, friend))
                if "Follow" in param:
                    data = json.loads(param)
                    name = data['Follow']['Name']
                    await asyncio.sleep(5)
                    asyncio.create_task(auto_invite_follow(name))
                if "Share post" in param:
                    data = json.loads(param)
                    post = data["Share post"]['post']
                    group = data["Share post"]['group']
                    page = data["Share post"]['page']
                    friends = data["Share post"]['friends']
                    content = data["Share post"]['content']

                    await asyncio.sleep(5)
                    asyncio.create_task(fb_share_post(post,friends,group,page,content))
                # if 'Stop' in param:
                #     # flagstop = True
                #     browser.quit()
                #     sys.exit()
async def main():
    task_1 = asyncio.create_task(listen())
    await task_1

if __name__ == '__main__':
    asyncio.run(main())
