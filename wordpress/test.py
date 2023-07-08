
from selenium import webdriver
from openpyxl import load_workbook
from time import sleep
from selenium.webdriver.common.keys import Keys
import random
import pandas as pd

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome('/Users/khangnt/Downloads OneDrive/chromedriver_mac_arm64/chromedriver', options=options)

def wait():
    return sleep(random.randint(5,8))


browser.get("http://hmmobilehanoi.com/wp-admin/edit.php?post_type=product")
wait()

id = browser.find_element_by_xpath('//*[@id="user_login"]')
id.send_keys("kythuat.hbweb@gmail.com")
pwd = browser.find_element_by_xpath('//*[@id="user_pass"]')
pwd.send_keys("Hbweb.vn@12345")
pwd.send_keys(Keys.ENTER)

sleep(3)

button = browser.find_element_by_xpath('//*[@id="menu-posts-product"]/a/div[3]')
# Click the button
button.click()

sleep(3)


# Click button Sản phẩm
button = browser.find_element_by_xpath('//*[@id="menu-posts-product"]/a/div[3]')
# Click the button
button.click()

file_path = '/Users/khangnt/Downloads/DanhSachAnh/kệ giá trang trí/từ khóa kệ trang trí.xls'
df = pd.read_excel(file_path)


for data in df["Keyword kệ trang trí"]:

    # Click button Thêm mới
    button = browser.find_element_by_xpath('//*[@id="wpbody-content"]/div[6]/a[1]')
    # Click the button
    button.click()

    sleep(1)

    id = browser.find_element_by_xpath('//*[@id="title"]')
    id.send_keys(data)

    sleep(1)

    button = browser.find_element_by_xpath('// *[ @ id = "in-product_cat-2055"]')
    # Click the button
    button.click()

    sleep(1)

    button = browser.find_element_by_xpath('//*[@id="publish"]')
    # Click the button
    button.click()



browser.quit()