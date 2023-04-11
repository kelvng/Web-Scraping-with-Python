import json
import random
import sys
from datetime import datetime
import time
import pandas as pd
import urllib.request

import requests
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from azcaptchaapi import AZCaptchaApi
from tqdm import tqdm
import websockets
import asyncio
from websocket import create_connection
from pynput import keyboard
# spider_name
name = 'Tailieu'
some_attribute = "Yes|No"
# Thông tin đăng nhập
Username = 'Langnghiem79'
Password = 'Langnghiem79'
starttime = time.time()
# Đường dẫn đến driver của webdriver
# Đường dẫn đến driver của webdriver
driver_path = r'C:\Users\Admin\PycharmProjects\Source\msedgedriver.exe'

# Đường dẫn đến list sản phẩm cần download, dạng file csv
list_products_path = r'C:\Users\Admin\PycharmProjects\Source\Webscarapy\Webscarapy\products-test.csv'

# Vị trí download, đường dẫn phải tồn tại thì mới có thể tải về được
download_dir = r'C:\Users\Admin\PycharmProjects\Source\Webscarapy\download'

# API key của bên giải quyết captcha
API_KEY = 'lzqixvjq2byp9zuxahp5dkwfnf1jsy8v'

api = AZCaptchaApi(API_KEY)


def delay():
    sleep(random.randint(3, 5))


# 1. Khai bao bien browser
options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2, "download.default_directory": download_dir}
options.add_experimental_option("prefs", prefs)
options.add_argument("--start-maximized")
options.add_argument("log-level=3")
# options.add_argument("--headless")
browser = webdriver.Edge(driver_path, options=options)

start_time = datetime.now()
list_url = []
list_file_download = []



def login():
    # 2. Mở web
    browser.get("https://tailieu.vn/")
    # 2a. Điền thông tin vào ô user và pass
    # Click vào button đăng nhập
    WebDriverWait(browser, 60).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[5]/span/span'))).click()
    # Click vào đăng nhập bằng tài khoản Tailieu.vn
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[18]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/p[2]'))).click()
    sleep(1)
    # Nhập tài khoản, mật khẩu
    txtLoginUsername = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "txtLoginUsername")))
    txtLoginUsername.click()
    txtLoginUsername.send_keys(Username)

    txtLoginPassword = browser.find_element_by_id("txtLoginPassword")
    txtLoginPassword.click()
    txtLoginPassword.send_keys(Password)
    # 2b. Submit form
    txtLoginPassword.send_keys(Keys.ENTER)
    sleep(5)


def logout():
    # 5. Logout tài khoản sau khi hoàn thành
    action = ActionChains(browser)
    account_info = browser.find_element_by_css_selector('#header > div.wrapheader > div.login > ul > li')
    action.move_to_element(account_info)
    action.perform()
    log_out_btn = browser.find_element_by_css_selector(
        '#header > div.wrapheader > div.login > ul > li > ul > li:nth-child(7) > a')
    log_out_btn.click()

# 3. Chạy login vào link tailieu.vn


# 4. loop qua các đường link sản phẩm
products_data = pd.read_csv(list_products_path)

# Note: trong file phải có sẵn cột download status để khi dùng chỉ lấy những link chưa được download
# nếu file dùng lần đầu thì uncomment dòng dưới để tự động add cột dowload status vào file và nhớ comment lại cho những lần dùng sau
# nếu không comment với file đã sử dụng, value mới sẽ bị đè vào và những file đã được download rồi sẽ bị download lại lần nữa
# products_data['download'] = np.nan
# lọc ra những link cần download
to_dowload = products_data.loc[products_data['download'] != 'Yes']
to_dowload = to_dowload.loc[to_dowload['download'] != 'Die']['Link'].head(5)  # số lượng file cần download

def trigger():
    async def main2():
        task_1 = asyncio.create_task(listen())
        task_2 = asyncio.create_task(download())
        await task_1
        await task_2
    if __name__ == '__main__':
        asyncio.run(main2())

async def listen():
    ws = websockets.connect('ws://127.0.0.1:9091',ping_interval=None)
    async with ws as wb:
        while True:
            msg = await wb.recv()
            print('listen  :' + ' ' + msg)
            if msg == 'Stop':
                # flagstop = True
                sys.exit()
            if msg == 'Start https://tailieu.vn/ /PythonCrawler/InsertCrawlerRunningLog':
                trigger()
async def main():
    task_1 = asyncio.create_task(listen())
    await task_1
    #await task_2

if __name__ == '__main__':
    asyncio.run(main())

async def download():
    #await.sleep()
    count_time = 0
    count_pass_captcha = 0
    options = webdriver.EdgeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2, "download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--start-maximized")
    options.add_argument("log-level=3")
    # options.add_argument("--headless")
    browser = webdriver.Edge(driver_path, options=options)
    browser.get("https://tailieu.vn/")
    # 2a. Điền thông tin vào ô user và pass
    # Click vào button đăng nhập
    WebDriverWait(browser, 60).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[5]/span/span'))).click()
    # Click vào đăng nhập bằng tài khoản Tailieu.vn
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[18]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/p[2]'))).click()
    await asyncio.sleep(1)
    # Nhập tài khoản, mật khẩu
    txtLoginUsername = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "txtLoginUsername")))
    txtLoginUsername.click()
    txtLoginUsername.send_keys(Username)

    txtLoginPassword = browser.find_element_by_id("txtLoginPassword")
    txtLoginPassword.click()
    txtLoginPassword.send_keys(Password)
    # 2b. Submit form
    txtLoginPassword.send_keys(Keys.ENTER)
    await asyncio.sleep(3)
    ws = websockets.connect('ws://127.0.0.1:9091',ping_interval=None)
    async with ws as wb:
        for product in tqdm(to_dowload):
            await asyncio.sleep(5)
            await wb.send(product)

            browser.get(product)
            list_url.append({"url": product})
            # đề phòng trường hợp đến lúc lên download mà link đó đã chết rồi, nên kiểm tra xem link sản phẩm còn tồn tại không
            try:
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#mainContent > div.con660.mh250 > div.margin405 > div.pnfright > p')))
                products_data.loc[products_data['Link'] == product, 'download'] = 'Die'
                products_data.to_csv("..\\products-test.csv")
            except:
                # print("Page available")
                list_file_download.append({"file_path": product})
                # click vào download:

                WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div[3]/div[3]/div[1]/div/a'))).click()

                WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lnkSubmitDL"]')))

                captcha = True
                while captcha:
                    # print("get page source")
                    page_source = browser.page_source

                    # print("find captcha image")
                    soup = BeautifulSoup(page_source, 'lxml')

                    links_captcha_img = soup.find_all("span", {"id": "spm_DocImgCaptchaDL"})[0].img['src']
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
                    count_pass_captcha += 1
                    try:
                        WebDriverWait(browser, 3).until(EC.alert_is_present())
                        alert = browser.switch_to.alert
                        alert.accept()
                        # print("\nwrong captcha")
                        # áp dụng delay tránh trường hợp code chạy nhanh hơn quá trình reload hình ảnh captcha
                        delay()

                    except TimeoutException:
                        captcha = False
                # 4a. click vào ô download của sản phẩm
                try:
                    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                                 '/html/body/div[5]/div/div[1]/div[1]/div/div/span[1]/div[2]/div/div/div/ul/li/p/span/span[2]/span/a'))).click()
                    products_data.loc[products_data['Link'] == product, 'download'] = 'Yes'
                    products_data.to_csv("..\\products-test.csv")

                except:
                    logout()
                    browser.quit()
                    browser = webdriver.Chrome(driver_path, options=options)
                    browser.get("https://tailieu.vn/")
                    login()

            count_time += 1
            if count_time == 10:
                await asyncio.sleep(2)
                logout()
                browser.quit()
                browser = webdriver.Edge(driver_path, options=options)
                browser.get("https://tailieu.vn/")
                login()




products_data.to_csv(list_products_path, index=False)
# sau khi kéo đến hết những file cần download thì check xem có file nào chưa tải hoàn thành thì đợi download hoàn thành
sleep(2)
logout()
# 6. Đóng trình duyệt
sleep(2)
domain = "https://tailieu.vn/"
endtime = datetime.now()
end_time = endtime.strftime("%H:%M:%S")
end_time = end_time.replace(":", "_")
# Insert data
time_scan = str(time.time() - starttime)
time_scan = time_scan[:-15]
time_scan = time_scan.replace(".", " ")
list_file_download = json.dumps(list_file_download)
list_url = json.dumps(list_url)

# data = {
#     'SessionCode': domain + end_time,
#     'StartTime': start_time,
#     'EndTime': endtime,
#     'UrlScanJson': list_url,
#     'FileDownloadJson': list_file_download,
#     'NumOfFile': count_time,
#     'FileResultData': '',
#     'NumPasscap': count_pass_captcha,
#     'UserIdRunning': '001',
#     'Ip': '1',
#     'Status': 'active',
#     'BotCode': 'tailieu.vn',
#     'TimeScan': time_scan,
#     'CreatedBy': 'admin',
# }
# url_upload = "http://localhost:6023/PythonCrawler/InsertCrawlerRunningLog"
# resp = requests.post(url_upload, data=data)
# if resp.ok:
#     print("Upload completed successfully!")
#     print(resp.text)
# else:
#     print("Something went wrong!")
browser.quit()
exit()