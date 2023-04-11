from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import random
import pandas as pd


name = 'TaiLieu'
some_attribute = "Yes|No"

def delay():
    sleep(random.randint(3,5))

# 1. Khai bao bien browser
options = webdriver.ChromeOptions()
p = {'download.default_directory':'C:\\Users\\pycha\\Downloads'}
options.add_experimental_option("prefs",p)
options.add_argument("start-maximized")
browser = webdriver.Chrome('C:\\Users\\pycha\\PycharmProjects\\Source\\chromedriver97.exe', options=options)


# 2. Mở web
browser.get("https://tailieu.vn/")
sleep(2)
# 2a. Điền thông tin vào ô user và pass
#Click vào button đăng nhập
browser.find_element_by_xpath('/html/body/div[4]/div/div[5]/span/span').click()
sleep(2)
#Click vào đăng nhập bằng tài khoản Tailieu.vn
browser.find_element_by_xpath('/html/body/div[18]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/p[2]').click()
sleep(1)
#Nhập tài khoản, mật khẩu
txtLoginUsername = browser.find_element_by_id("txtLoginUsername")
txtLoginUsername.send_keys("Langnghiem79 ")

txtLoginPassword = browser.find_element_by_id("txtLoginPassword")
txtLoginPassword.send_keys("Langnghiem79 ")

# 2b. Submit form

txtLoginPassword.send_keys(Keys.ENTER)

sleep(5)

# 3. Kiểm tra captcha có xuất hiện không?


# 4. loop qua các đường link sản phẩm
products_data = pd.read_csv('C:\\Users\\pycha\\PycharmProjects\\Source\\learn_scrapy\\products-test.csv')
for product in tqdm(products_data['Link'].tolist()):
    browser.get(product)
    # 4a. click vào ô download của sản phẩm
    browser.find_element_by_xpath('/html/body/div[6]/div/div[3]/div[3]/div[1]/div/a').click()
   # browser.find_element_by_xpath('/html/body/section/div[3]/div[1]/div/div[1]/div[1]/div[1]/div[4]/button').click()
    #sleep(10)
#5. Xử lý captcha
    WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[name^='a-'][src^='x?']")))
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//span[@class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox']/div[@class='recaptcha-checkbox-border']"))).click()
# Xác nhận download
    browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div/span/form/div[1]/ul/li/div[2]').click()
    browser.find_element_by_xpath("//div[@id='linkdownload']/p/a[@target='downbtl']").click()

    browser.find_element_by_xpath('/html/body/div[13]/div[1]/div[1]/div/div/div/div/div/div[1]/div[1]/div[1]/p/a').click()

    browser.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/span/div[2]/div/div/div/ul/li/p/span/span[2]/span').click()
# 5. Dừng chương trình 5 giây
    sleep(2)

# 6. Đóng trình duyệt
browser.quit()