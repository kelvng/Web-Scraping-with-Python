from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import facebook_scraper
import numpy as np
from tqdm import tqdm
import random

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
# options.add_argument("--headless")
browser = webdriver.Chrome(r'C:\Users\Admin\PycharmProjects\Source\chromedriver.exe', options=options)


def wait():
    return sleep(random.randint(8,12))


def xpath_soup(element):
# https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
# function để có lấy full đường dẫn xpath tới vị trí mình mong muốn
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


browser.get("https://www.facebook.com")
wait()
#zetabase3i@gmail.com Langnghiem@79
username = "nguyenvanhuy10a3@gmail.com"
password = "AD123456"

# login to facebook
id = browser.find_element_by_xpath('//*[@id="email"]')
id.send_keys(username)
pwd = browser.find_element_by_xpath('//*[@id="pass"]')
pwd.send_keys(password)
pwd.send_keys(Keys.ENTER)

#def get_all_self_groups(browser):

    # ấn vào my profile
browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div[1]/div[4]/a/span/span').click()

wait()

    # chuyển đường dẫn tới trang nhóm của bản thân
groups_page = browser.current_url + '&sk=groups'

browser.get(groups_page)

wait()

    # kéo tới cuối trang để load tất cả các group
reached_page_end = Falselast_height = browser.execute_script("return document.body.scrollHeight")

while not reached_page_end:
        browser.find_element_by_xpath('//body').send_keys(Keys.END)
        sleep(2)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
                reached_page_end = True
        else:
                last_height = new_height

wait()

    # lấy content của web rồi pass qua beatifulsoup
page_source = browser.page_source
soup = bs(page_source, 'lxml')

links = []

    # tìm tất cả đường link của các group
page_groups = soup.find("div", {"data-pagelet":"ProfileAppSection_0"})
for s in page_groups.find_all('a'):
        try:
            link = s['href']
            if 'groups' in link and 'profile.php' not in link:
                links.append(link)
        except:
            pass

links = list(set(links))

    # export qua file npy hoặc có thể sử dụng định dạng khác nếu muốn
save_links = np.array(links)
np.save('group_links.npy', save_links)

wait()

def get_post_link_group(path_to_groups_link, ID, PW):
    # thông tin đăng nhập của tài khoản cần dùng
    credential = (ID, PW)

    group_links = np.load(path_to_groups_link)

    links_post = []

    # loop qua các đường link của group rồi dùng facebook_scraper extract link post
    # facebook_scraper: https://pypi.org/project/facebook-scraper/
    for link in group_links:
        group_id = link.split(".")[-2]

        for post in tqdm(facebook_scraper.get_posts(group=group_id,credentials=credential, pages=3)):
            if 'permalink' in post['post_url']:
                links_post.append(post['post_url'].replace("m.", ""))

    # save file chứa link post
    links_post = np.array(links_post)
    np.save("post_links.npy", links_post)

def auto_post_group(path_to_group_links, comment):
    # get list of group links
    group_links = np.load(path_to_group_links)
    for link in group_links:
        browser.get(link)
        wait()

        # lấy dữ liệu từ page source để xử lý
        page_source = browser.page_source
        soup = bs(page_source, 'lxml')

        # tìm vị trí của box post bài
        # tuỳ vào ngôn ngữ mà text có thể khác nhau, việc lấy text phải làm manual
        post_box = xpath_soup(soup.body.find(text="Tạo bài viết công khai...").parent)

        browser.find_element_by_xpath(post_box).click()
        wait()

        type_box = browser.find_element_by_xpath(xpath_soup(soup.find("div", {"aria-label": "Tạo bài viết công khai..."})))
        type_box.click()
        type_box.send_keys(comment)

        submit_bt = browser.find_element_by_xpath(xpath_soup(soup.find("div", {"aria-label": "Đăng"})))
        submit_bt.click()

        wait()

def auto_like_and_comment_post(path_to_post_links, comment):
    # load file chứa link post
    links_post = np.load(path_to_post_links)

    #loop qua các link để thực hiện việc like và comment
    for link in links_post:
        browser.get(link)

        sleep(wait())

        page_source = browser.page_source
        soup = bs(page_source, 'lxml')

        # tìm ô like theo nhãn, tuỳ theo ngôn ngữ mà sẽ khác nhau. Việc tìm nhãn phải làm manual
        like = soup.find("div", {"aria-label":"Thích"})
        like = browser.find_element_by_xpath(xpath_soup(like))
        like.click()
        wait()

        # tương tự như thế với ô comment
        comment_box = soup.find_all("div", {"aria-label":"Viết bình luận"})[-1]
        comment_box = browser.find_element_by_xpath(xpath_soup(comment_box))
        comment_box.click()
        wait()

        comment_box.send_keys(comment)
        wait()

        comment_box.send_keys(Keys.ENTER)
        wait()


wait()
browser.quit()