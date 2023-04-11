from selenium import webdriver
from time import sleep
from tqdm import tqdm
import pandas as pd

name = 'VNDOC'
some_attribute = "Yes|No"
# 1. Khai bao bien browser
options = webdriver.ChromeOptions()
p = {'download.default_directory':'F:\Download'}
options.add_experimental_option("prefs",p)
options.add_argument("start-maximized")
browser = webdriver.Chrome('/chromedriver97.exe', options=options)
# 2. Mở web
browser.get("https://vndoc.com/")
# 4. loop qua các đường link sản phẩm
products_data = pd.read_csv('/learn_scrapy/products.csv')
for product in tqdm(products_data['Link'].tolist()):
    print(product)
    browser.get(product)
    sleep(2)
    # 4a. click vào ô download của sản phẩm

    browser.find_element_by_xpath('/html/body/div/div/div[5]/a').click()
    sleep(1)
    browser.find_element_by_xpath('/html/body/div/div/div[1]/div[1]/a').click()
# 5. Dừng chương trình 5 giây
#sleep(5)
# 6. Đóng trình duyệt
browser.quit()