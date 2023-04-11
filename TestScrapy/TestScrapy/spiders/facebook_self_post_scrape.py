from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import facebook_scraper as fs
import json

options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome('../../../chromedriver97.exe', options=options)


browser.get("https://www.facebook.com")

# login to facebook
id = browser.find_element_by_xpath('//*[@id="email"]')
id.send_keys("zetabase3i@gmail.com")
pwd = browser.find_element_by_xpath('//*[@id="pass"]')
pwd.send_keys("Langnghiem@79")
pwd.send_keys(Keys.ENTER)

sleep(5)

# click on my profile
browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div[1]/div[4]/a/span/span').click()

sleep(5)

# scroll all the way down
reached_page_end = False
last_height = browser.execute_script("return document.body.scrollHeight")

while not reached_page_end:
      browser.find_element_by_xpath('//body').send_keys(Keys.END)   
      sleep(2)
      new_height = browser.execute_script("return document.body.scrollHeight")
      if last_height == new_height:
            reached_page_end = True
      else:
            last_height = new_height

sleep(5)

# extract all post in wall links
page_source = browser.page_source
soup = bs(page_source, 'lxml')

links = []

page_timeline = soup.find("div", {"data-pagelet":"ProfileTimeline"})
for s in page_timeline.find_all('a'):
      link = s['href']
      if 'permalink.php' in link:
            if not "substory" in link and not "comment" in link:
                  links.append(link)

# scrape all the post
fs_options = {'comments': True}
for link_post in links:
      for post in fs.get_posts(link_post, options=fs_options):
            with open('{}.json'.format(post['post_id']), 'w') as f:
                  json.dump(post, f, default=str, indent=1)

browser.quit()