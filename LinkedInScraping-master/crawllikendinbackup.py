# Import libraries and packages for the project
import json
from tqdm import tqdm
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
import os, random
import glob
from docx import Document
print('- Finish importing packages')

# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path=r'F:\PycharmProjects\Source\chromedriver.exe',
                           options=options)
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

#Task 1.2: Import username and password

mypath = r'F:\PycharmProjects\Source\LinkedInScraping-master\credential\*'
credrelist = glob.glob(mypath)

Credrelist = random.choice(credrelist) #change dir name to whatever
print(Credrelist)
credential = open(r'F:\PycharmProjects\Source\LinkedInScraping-master\credential\credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
print('- Finish importing the login credentials')
sleep(2)
#https://www.linkedin.com/search/results/people/?geoUrn=%5B%22104195383%22%2C%2290010187%22%2C%2290010186%22%2C%22103697962%22%2C%22100921423%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=FACETED_SEARCH&page=100&sid=.nH
# Task 1.2: Key in login credentials
email_field = driver.find_element_by_id('username')
email_field.send_keys(username)
print('- Finish keying in email')
sleep(3)

password_field = driver.find_element_by_name('session_password')
password_field.send_keys(password)
print('- Finish keying in password')
sleep(2)
# Task 1.2: Click the Login button
signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()

# keywords= ['VNPT','Global CyberSoft Việt Nam','Intel Corporation','Bkav']
# for keyword in keywords:
searc_url = input('search url contacrt: ')
driver.get(searc_url)


print('- Finish Task 1: Login to Linkedin')

# Task 2: Search for the profile we want to crawl
# Task 2.1: Locate the search bar element
#search_field = driver.find_element_by_xpath('//*[@class="search-global-typeahead__input always-show-placeholder"]')
# Task 2.2: Input the search query to the search bar
#search_query = input('What profile do you want to scrape? ')
#search_field.send_keys(keyword)

# Task 2.3: Search
#search_field.send_keys(Keys.RETURN)

print('- Finish Task 2: Search for profiles')


# Task 3: Scrape the URLs of the profiles
# Task 3.1: Write a function to extract the URLs of one page
all_profile_URL = []
def GetURL():
    sleep(2)
    page_source = BeautifulSoup(driver.page_source, 'lxml')
    try:

        page_source = page_source.find('div', class_="ph0 pv2 artdeco-card mb2")
        profiles = page_source.find_all('a', class_ = 'app-aware-link') #('a', class_ = 'search-result__result-link ember-view')
        for profile in profiles:
            # profile_ID = profile.get('href')
            # profile_URL = "https://www.linkedin.com" + profile_ID
            profile_URL = profile.get('href')
            if '/in/' in profile_URL:
                if profile_URL not in all_profile_URL:

                    all_profile_URL.append(profile_URL)
            else:
                pass
    except:
        pass
    print('Get url:' + str(all_profile_URL))

    return all_profile_URL


# Task 3.2: Navigate through many page, and extract the profile URLs of each page
input_page = int(input('How many pages you want to scrape: '))
#input_page = 100
URLs_all_page = []
dem = 0
for page in range(input_page):
    dem = dem + 1
    progess = (dem / input_page) * 100
    print(str(progess) + ' %')
    URLs_one_page = GetURL()

    sleep(1.5)
    cannot_click = driver.find_element_by_xpath(
        "//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary artdeco-button--disabled ember-view']")
    if cannot_click != None:
        break
    else:
        pass
    try:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
        sleep(1)
        next_button = driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']")
        #artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view
        driver.execute_script("arguments[0].click();", next_button)
        URLs_all_page = URLs_one_page

        sleep(2)
    except:
        continue

print('page: ' + str(URLs_all_page))
print('- Finish Task 3: Scrape the URLs')


for i in URLs_all_page:
    LinkUrl = i
    if '/profile-video' in LinkUrl:
        LinkUID = str(LinkUrl).split('/profile-video')[0]
        UID = LinkUID.replace('https://www.linkedin.com/in/','')
    elif '?miniProfileUrn' in LinkUrl:
        LinkUID = str(LinkUrl).split('?miniProfileUrn')[0]
        UID = LinkUID.replace('https://www.linkedin.com/in/', '')
    else:
        LinkUID = LinkUrl
        UID = LinkUID
    print(LinkUrl)
    print(LinkUID)
    print('-----------------------')
    datajson = {
        'ComputerCode':'QUARK4',
        'ProfileId':LinkUID,
        'LinkedInUrl':UID,
    }
    url_upload = "http://117.6.131.222:8989/PythonCrawler/InsertLinkedInUrl"
    # url_upload = "https://dieuhanh.vatco.vn/PythonCrawler/InsertCrawlerRunningLog"
    resp = requests.post(url_upload, data=datajson)
    if resp.ok:
        print("Upload completed successfully!")
        print("data report crawl!")
        print(resp.text)
    else:
        print("Something went wrong!")
        #writer.writerow({headers[0]: LinkUrl})

