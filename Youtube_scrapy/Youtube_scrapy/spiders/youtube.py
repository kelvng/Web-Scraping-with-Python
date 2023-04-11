
import pandas as pd
from selenium.webdriver.common.keys import Keys
from time import sleep
from tqdm import tqdm
from pywinauto.application import Application
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random

name = 'youtube'
some_attribute = "Yes|No"
x = input("bạn muốn chạy : ")

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome('E:\Source\chromedriver97.exe', options=options)

def wait():
    return sleep(random.randint(4,6))

'''target link trình duyệt'''
browser.get(
    "https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
wait()

'''login to youtube'''
email = "bot3i12345@gmail.com"
password = "bot3i12345@1234"
id = browser.find_element_by_xpath('//*[@autocomplete="username"]')
id.send_keys(email)

sleep(2)
browser.find_element_by_xpath('//*[@id="identifierNext"]').click()
sleep(2)
pwd = browser.find_element_by_xpath('//*[@autocomplete="current-password"]')
pwd.send_keys(password)
sleep(1)
browser.find_element_by_xpath('//*[@jsname="LgbsSe"]').click()
sleep(2)

         '''to clean popups after login'''

def youtube_auto_comment():
    '''Lấy link bài viết từ file csv'''
    products_data = pd.read_csv('E:\Source\Youtube_scrapy\Youtube_scrapy\Link_Video.csv')
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
         '''tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual'''

        sleep(5)
        browser.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
        sleep(5)
        browser.find_element_by_xpath('//*[@id="placeholder-area"]').click()
        sleep(2)
        item = browser.find_element_by_xpath('//*[@id="contenteditable-root"]')
        comment = "I like it!\n This is the most amazing things ever seen.\n Wanna see more~\n"
        item.send_keys(comment)
        item.send_keys(Keys.CONTROL, Keys.ENTER)

        wait()
        browser.quit()

def youtube_auto_subscribe():
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no save Info")
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no notification box")

             '''Lấy link bài viết từ file csv'''
    products_data = pd.read_csv('E:\Source\Youtube_scrapy\Youtube_scrapy\Link_Video.csv')
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
                 '''tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual'''

        sleep(3)
        browser.find_element_by_xpath('//*[@class="style-scope ytd-subscribe-button-renderer"]').click()
        try:
            sleep(1)
            comment_box = browser.find_element_by_xpath('//*[@aria-label="Tweet text"]')
            sleep(2)
            comment_box.send_keys("Good")
            wait()
            browser.find_element_by_xpath('//*[@data-testid="tweetButton"]').click()
            wait()
        except:
            wait()

                # finally:
                # browser.find_element_by_xpath('//*[@aria-label="Gỡ Thích"]').click()
                # wait()
    sleep(1)
    browser.quit()


def youtube_auto_unsubscribe():
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no save Info")
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no notification box")

            ''' Lấy link bài viết từ file csv'''
    products_data = pd.read_csv('E:\Source\Youtube_scrapy\Youtube_scrapy\Link_Video.csv')
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
                ''' tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual'''

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

def youtube_auto_like():
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no save Info")
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no notification box")

            ''' Lấy link bài viết từ file csv'''
    products_data = pd.read_csv('E:\Source\Youtube_scrapy\Youtube_scrapy\Link_Video.csv')
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
                 '''tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual'''

        sleep(3)
        browser.find_element_by_xpath("//*[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a").click()
        try:
            sleep(1)
            comment_box = browser.find_element_by_xpath('//*[@aria-label="Tweet text"]')
            sleep(2)
            comment_box.send_keys("Good")
            wait()
            browser.find_element_by_xpath('//*[@data-testid="tweetButton"]').click()
            wait()
        except:
            wait()

                # finally:
                # browser.find_element_by_xpath('//*[@aria-label="Gỡ Thích"]').click()
                # wait()
    sleep(1)
    browser.quit()

def youtube_auto_unlike():
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no save Info")
    try:
        browser.find_element_by_xpath("//*[contains(@class, 'aOOlW   HoLwm ')]").click()
    except NoSuchElementException:
        print("no notification box")

             '''Lấy link bài viết từ file csv'''
    products_data = pd.read_csv('E:\Source\Youtube_scrapy\Youtube_scrapy\Link_Video.csv')
    for product in tqdm(products_data['Link'].tolist()):
        browser.get(product)
                 '''tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual'''

        sleep(3)
        browser.find_element_by_xpath("//*[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a").click()
        try:
            sleep(1)
            comment_box = browser.find_element_by_xpath('//*[@aria-label="Tweet text"]')
            sleep(2)
            comment_box.send_keys("Good")
            wait()
            browser.find_element_by_xpath('//*[@data-testid="tweetButton"]').click()
            wait()
        except:
            wait()

                # finally:
                # browser.find_element_by_xpath('//*[@aria-label="Gỡ Thích"]').click()
                # wait()
    sleep(1)
    browser.quit()
def youtube_auto_post():
    filepath = 'E:\Source\Youtube_scrapy\Youtube_scrapy\spiders\Video1.mp4'
    # if title is not in data, return immediately
    # navigate to the upload page
    browser.get('https://studio.youtube.com/')
    # click on 'Create' button
    browser.find_element_by_id('create-icon').click()
    # Click on 'Upload Video'
    browser.find_element_by_xpath(
       '//div[contains(text(), "Upload videos")]').click()
    browser.find_element_by_xpath(
        '//div[contains(text(), "Select files")]').click()
    # Get Input Element
    # Title
    sleep(2)
    upload_dialog = Application().connect(title_re='Open')
    upload_dialog.Open.Edit.type_keys(filepath)
    sleep(5)
    upload_dialog.window(title_re='Open').Open.click()
    sleep(3)
    browser.find_element_by_xpath('//*[@name="VIDEO_MADE_FOR_KIDS_MFK"]').click()
    # Next
    browser.find_element_by_id('next-button').click()
    browser.find_element_by_id('next-button').click()
    browser.find_element_by_id('next-button').click()

    visibilities = ['PUBLIC', 'UNLISTED', 'PRIVATE']
    browser.find_element_by_xpath('//*[@name="' + visibilities[0] + '"]').click()
    # Done
    browser.find_element_by_id('done-button').click()
def youtube_auto_search():
    try:
        key_search = "Elonmust"
        browser.find_element_by_xpath('//*[@id="search-form"]').click()
        sleep(1)
        search = browser.find_element_by_xpath('//*[@aria-label="Search"]')
        search.send_keys(key_search)
        sleep(1)
        search.send_keys(Keys.ENTER)

        #browser.quit()
    except:
        pass

if x == 'post':
     youtube_auto_post()
if x == 'comment':
    youtube_auto_comment()
if x == 'subscribe':
    youtube_auto_subscribe()
if x == 'unsubscribe':
    youtube_auto_unsubscribe()
if x == 'like':
    youtube_auto_like()
if x == 'unlike':
    youtube_auto_unlike()
if x == 'search':
     youtube_auto_search()