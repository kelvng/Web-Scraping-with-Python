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

# Task 1.2: Import username and password

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
print('- Finish Loggin')



keywords= ['VNPT','Global CyberSoft Việt Nam','Intel Corporation','Bkav']
for keyword in keywords:
    url = 'https://www.linkedin.com'
    driver.get(url)
    sleep(3)

    print('- Finish Task 1: Login to Linkedin')

    # Task 2: Search for the profile we want to crawl
    # Task 2.1: Locate the search bar element
    search_field = driver.find_element_by_xpath('//*[@class="search-global-typeahead__input always-show-placeholder"]')
    # Task 2.2: Input the search query to the search bar
    #search_query = input('What profile do you want to scrape? ')
    search_field.send_keys(keyword)

    # Task 2.3: Search
    search_field.send_keys(Keys.RETURN)

    print('- Finish Task 2: Search for profiles')


    # Task 3: Scrape the URLs of the profiles
    # Task 3.1: Write a function to extract the URLs of one page
    all_profile_URL = []
    def GetURL():
        page_source = BeautifulSoup(driver.page_source, 'lxml')
        sleep(3)
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
        print('Get url:' + str(all_profile_URL))
        return all_profile_URL


    # Task 3.2: Navigate through many page, and extract the profile URLs of each page
    input_page = int(input('How many pages you want to scrape: '))

    URLs_all_page = []
    dem = 0
    for page in range(input_page):
        dem = dem + 1
        progess = (dem / input_page) * 100
        print(str(progess) + ' %')
        URLs_one_page = GetURL()
        sleep(2)
        try:
            sleep(2)
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


    # Task 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file
    with open('normalurl.csv', 'w',  newline = '',encoding="utf-8") as file_output:
        headers = ['PROFILEURL']
        writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
        writer.writeheader()
        for i in URLs_all_page:

            LinkUrl = i
            writer.writerow({headers[0]: LinkUrl})

