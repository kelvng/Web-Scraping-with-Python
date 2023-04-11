from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import random
import pandas as pd



name = 'Envato'
some_attribute = "Yes|No"
def delay():
    sleep(random.randint(3,5))

# 1. Khai bao bien browser
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome('chromedriver97.exe', options=options)


# 2. Mở web
browser.get("https://elements.envato.com/sign-in")

# 2a. Điền thông tin vào ô user và pass

txtUser = browser.find_element_by_id("signInUsername")
txtUser.send_keys("jackbot123")

txtPass = browser.find_element_by_id("signInPassword")
txtPass.send_keys("envato12345")

# 2b. Submit form

txtPass.send_keys(Keys.ENTER)

sleep(5)

# 3. Kiểm tra captcha có xuất hiện không?

def check_exits_by_xpath(xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

recaptcha_frame = '//*[@id="app"]/div[1]/main/div/div/div[2]/div/div/div[2]/form/div[4]/div/div/div/div/div/iframe'
check_box_bt = '//*[@id="recaptcha-anchor"]/div[1]'
challenge_frame = '/html/body/div[9]/div[4]/iframe'
solve_bt = '//*[@id="solver-button"]'

if check_exits_by_xpath(recaptcha_frame):

    # 3a. Tìm frame captcha và click vào xác nhận
    browser.switch_to.frame(browser.find_element_by_xpath(recaptcha_frame))

   # browser.find_element_by_xpath(check_box_bt).click()

    sleep(3)
    browser.switch_to.default_content()

    # 3b. Nếu có challenge xuất hiện thì ấn vào nút giải challenge của extension
    if check_exits_by_xpath(challenge_frame):
        browser.switch_to.frame(browser.find_element_by_xpath(challenge_frame))
        browser.find_element_by_xpath(solve_bt).click()
        sleep(5)

    # 3c. Click vào "Login"
    browser.find_element_by_xpath('//*[@id="app"]/div[1]/main/div/div/div[2]/div/div/div[2]/form/button/div/span').click()

    sleep(5)

# 4. loop qua các đường link sản phẩm
products_data = pd.read_csv('learn_scrapy/products.csv')
for product in tqdm(products_data['Link'].tolist()):
    browser.get(product)
    sleep(5)
    # 4a. click vào ô download của sản phẩm
    browser.find_element_by_xpath('//*[@id="app"]/div[1]/main/div/div[2]/div/div[2]/button/div').click()
    sleep(3)
    browser.find_element_by_xpath('/html/body/div[8]/div/div/div/form/div/div/label/span[1]').click()
    browser.find_element_by_xpath('/html/body/div/div/div/div/form/div/button').click()
    sleep(3)

    # 4b. kiểm tra xem có captcha không và click vào ô check box
    captcha_frame = '/html/body/div[12]/div/div/div/div/div/form/div[1]/div[2]/div[2]/div/div/div/div/div/iframe'
    check_bt = '//*[@id="recaptcha-anchor"]/div[1]'
    captcha_challenge_frame = '/html/body/div[10]/div[4]/iframe'
    solve_bt_2 = '//*[@id="solver-button"]'

    if check_exits_by_xpath(captcha_frame):
        browser.switch_to.frame(browser.find_element_by_xpath(captcha_frame))
        browser.find_element_by_xpath(check_bt).click()

        sleep(3)
        browser.switch_to.default_content()


        # 4c. nếu có challenge, làm tương tự và giải challenge
        challenge_frame = '/html/body/div[9]/div[4]/iframe'
        solve_bt = '//*[@id="solver-button"]'
        if check_exits_by_xpath(challenge_frame):
            browser.switch_to.frame(browser.find_element_by_xpath(challenge_frame))
            browser.find_element_by_xpath(solve_bt).click()
            sleep(5)
            browser.switch_to.default_content()
            if check_exits_by_xpath(captcha_frame):
                browser.switch_to.frame(browser.find_element_by_xpath(captcha_challenge_frame))
                browser.find_element_by_xpath(solve_bt_2).click()
                sleep(5)
                browser.switch_to.default_content()
                browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div/div/form/div[2]/button').click()
                sleep(3)


# 5. Dừng chương trình 5 giây
sleep(5)

# 6. Đóng trình duyệt
browser.quit()