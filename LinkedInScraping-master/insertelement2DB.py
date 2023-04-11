# Import libraries and packages for the project
import glob
import json
import random

import numpy as np
import pandas as pd
import csv
from tqdm import tqdm
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
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
mypath = r'F:\PycharmProjects\Source\LinkedInScraping-master\credential\*'
credrelist = glob.glob(mypath)

Credrelist = random.choice(credrelist) #change dir name to whatever
print(Credrelist)

# Task 1.2: Import username and password
credential = open(r'F:\PycharmProjects\Source\LinkedInScraping-master\credential\credentials8.txt')
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
sleep(3)

print('- Finish Task 1: Login to Linkedin')

products_data = pd.read_csv(
    r'F:\PycharmProjects\Source\LinkedInScraping-master\MainFILE.csv')
#products_data['download'] = np.nan
to_dowload = products_data.loc[products_data['download'] != 'Yes']
to_dowload = to_dowload.loc[to_dowload['download'] != 'checkagain']
list_link = to_dowload.loc[to_dowload['download'] != 'Die']['PROFILEURL'].head(300)

for link in tqdm(list_link):
    driver.get(link)
    print('- Accessing profile: ', link)
    sleep(3)
    Linkedin = driver.current_url
    page_source = BeautifulSoup(driver.page_source, "html.parser")
    info_div = page_source.find('body')
    try:
        check = info_div.find('section', class_="artdeco-card ember-view pv-top-card")
        check_text = check.get_text()
    except:
        products_data.loc[products_data['PROFILEURL'] == link, 'download'] = 'checkagain'
        products_data.to_csv(
            r"F:\PycharmProjects\Source\LinkedInScraping-master\MainFILE.csv")
        print('ACCOUNT HAS been detect')
        break
    # Name = info_div.find('h1',
    #                      class_="text-heading-xlarge inline t-24 v-align-middle break-words").get_text().strip()  # Remove unnecessary characters
    # print('--- Profile name is: ', Name)
    print(Linkedin)

    Element = str(info_div)
    # soup = BeautifulSoup(Element,"html.parser")
    # info_div1 = soup.find('body')
    # Name = info_div1.find('h1',
    #                      class_="text-heading-xlarge inline t-24 v-align-middle break-words").get_text().strip()  # Remove unnecessary characters
    # print('--- Profile name is: ', Name)

    jsondata = {
            'ProfileUrl':Linkedin,
            'ElementSite':Element
        }
    #print(jsondata)
    url_upload = "http://localhost:6023/PythonCrawler/InsertLinkedinLog"
    # url_upload = "https://dieuhanh.vatco.vn/PythonCrawler/InsertCrawlerRunningLog"
    resp = requests.post(url_upload, data=jsondata)
    if resp.ok:
        print("Upload completed successfully!")
        print("data report crawl!")
        print(resp.text)
    else:
        print("Something went wrong!")
    products_data.loc[products_data['PROFILEURL'] == link, 'download'] = 'Yes'
    products_data.to_csv(
        r"F:\PycharmProjects\Source\LinkedInScraping-master\MainFILE.csv")

# # Task 2: Search for the profile we want to crawl
# # Task 2.1: Locate the search bar element
# search_field = driver.find_element_by_xpath('//*[@class="search-global-typeahead__input always-show-placeholder"]')
# # Task 2.2: Input the search query to the search bar
# search_query = input('What profile do you want to scrape? ')
# search_field.send_keys(search_query)
#
# # Task 2.3: Search
# search_field.send_keys(Keys.RETURN)
#
# print('- Finish Task 2: Search for profiles')
#
#
# # Task 3: Scrape the URLs of the profiles
# # Task 3.1: Write a function to extract the URLs of one page
# all_profile_URL = []
# def GetURL():
#     page_source = BeautifulSoup(driver.page_source, 'lxml')
#     sleep(3)
#     profiles = page_source.find_all('a', class_ = 'app-aware-link') #('a', class_ = 'search-result__result-link ember-view')
#     for profile in profiles:
#         # profile_ID = profile.get('href')
#         # profile_URL = "https://www.linkedin.com" + profile_ID
#         profile_URL = profile.get('href')
#         if '/in/' in profile_URL:
#             if profile_URL not in all_profile_URL:
#
#                 all_profile_URL.append(profile_URL)
#         else:
#             pass
#     print('Get url:' + str(all_profile_URL))
#     return all_profile_URL
#
#
# # Task 3.2: Navigate through many page, and extract the profile URLs of each page
# input_page = int(input('How many pages you want to scrape: '))
#
# URLs_all_page = []
# for page in range(input_page):
#     URLs_one_page = GetURL()
#     sleep(2)
#     try:
#         sleep(2)
#         driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
#         sleep(1)
#         next_button = driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']")
#         #artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view
#         driver.execute_script("arguments[0].click();", next_button)
#         URLs_all_page = URLs_one_page
#
#
#         sleep(2)
#     except:
#         continue
#
# print('page: ' + str(URLs_all_page))
# print('- Finish Task 3: Scrape the URLs')


# Task 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file
# with open('output.csv', 'w',  newline = '',encoding="utf-8") as file_output:
#     headers = ['ProfileURL', 'Name', 'Contact', 'Location', 'Current_Job','About','Experience','Education',
#                'Skills','Languages','Interests','Licenses','Recommendations','Awards','Organizations','Activity']
#
#
#     writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
#     writer.writeheader()
#     #print(URLs_all_page)
#
#     #for linkedin_URL in URLs_all_page:
#     for linkedin_URL in tqdm(URLs_all_page):
#         try:
#             driver.get(linkedin_URL)
#             print('- Accessing profile: ', linkedin_URL)
#             sleep(3)
#             page_source = BeautifulSoup(driver.page_source, "html.parser")
#             info_div = page_source.find('body')
#             info_div = info_div.find('main', class_='scaffold-layout__main')
#             #print(info_div)
#             #try:
#             #Name of linkedin
#             Name = info_div.find('h1', class_= "text-heading-xlarge inline t-24 v-align-middle break-words").get_text().strip() #Remove unnecessary characters
#             print('--- Profile name is: ', Name)
#             Location = info_div.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip() #Remove unnecessary characters
#             print('--- Profile location is: ', Location)
#             Current_Job = info_div.find('div', class_='text-body-medium break-words').get_text().strip()
#             print('--- Job location is: ', Current_Job)
#             #all ifo finding
#             skillList = info_div.find_all('section', class_='artdeco-card ember-view relative break-words pb3 mt2')
#             #profile url
#             Linkedin = driver.current_url
#             print(Linkedin)
#
#             #print('--- list is : ', skillList)
#
#             About = ''
#             Experience = ''
#             Education = ''
#             Skills = ''
#             Languages = ''
#             Interests = ''
#             Licenses= ''
#             Recommendations=''
#             Awards = ''
#             Organizations = ''
#             Certifications = ''
#             Contact = ''
#             Activity = ''
#             for i in skillList:
#                 data_source = i
#                 data = data_source.get_text().strip()
#                 # print(data_source.get_text().strip())
#                 # print('------------------------------------------------------')
#                 # stirng = '---------------------------------------------------------'
#                 data = data.replace('\n\n\n\n\n', '\n')
#                 data = data.replace('\n\n\n\n', '\n')
#                 data = data.replace('\n\n\n','\n')
#                 data = data.replace('\n\n','\n')
#                 if 'AboutAbout' in data:
#                     aboutSource = data_source
#                     About_local = aboutSource.find_all('span', class_="visually-hidden")
#                     AboutList = []
#                     for i in About_local:
#                         data1 = i.get_text().strip()
#                         data1 = data1.replace('\n\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n', '\n')
#                         data1 = data1.replace('\n\n', '\n')
#                         About = data1
#                     #artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column
#                 elif 'ExperienceExperience' in data:
#                     experienceSource = data_source
#                     ExperienceList = []
#                     if 'Show all' in data:
#                         local = skillsSource.find('div', class_="pvs-list__footer-wrapper")
#                         geturl = local.find('a')['href']
#                         driver.get(geturl)
#                         sleep(2)
#                         Experience_local = driver.find_element_by_xpath('//*[@class="artdeco-card ember-view pb3"]')
#                         Experience_locals = Experience_local.find_elements_by_xpath('//*[@class="visually-hidden"]')
#                         for i in Experience_locals:
#                             data1 = i.get_text().strip()
#                             data1 = data1.replace('\n\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n', '\n')
#                             data1 = data1.replace('\n\n', '\n')
#                             ExperienceList.append(data1)
#                         Experience = '\n'.join(map(str, ExperienceList))
#                         ExperienceList.clear()
#                         pass
#                     else:
#
#                         # Experience_local = experienceSource.find_all('li',class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")
#                         Experience_local = experienceSource.find_all('span', class_='visually-hidden')
#
#                         for i in Experience_local:
#                             data1 = i.get_text().strip()
#                             data1 = data1.replace('\n\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n', '\n')
#                             data1 = data1.replace('\n\n', '\n')
#                             ExperienceList.append(data1)
#                         Experience = '\n'.join(map(str, ExperienceList))
#                         ExperienceList.clear()
#
#                 elif 'EducationEducation' in data:
#                     educationSource = data_source
#                     EducationList = []
#                     if 'Show all' in data:
#                         local = skillsSource.find('div', class_="pvs-list__footer-wrapper")
#                         geturl = local.find('a')['href']
#                         driver.get(geturl)
#                         sleep(2)
#                         Education_local = driver.find_element_by_xpath('//*[@class="artdeco-card ember-view pb3"]')
#                         Education_locals = Education_local.find_elements_by_xpath('//*[@class="visually-hidden"]')
#                         for i in Education_locals:
#                             data1 = i.get_text().strip()
#                             data1 = data1.replace('\n\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n', '\n')
#                             data1 = data1.replace('\n\n', '\n')
#                             EducationList.append(data1)
#                         Education = '\n'.join(map(str, EducationList))
#                         EducationList.clear()
#                         pass
#                     else:
#
#                         #Education_local = educationSource.find_all('li',class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")
#                         Education_local = educationSource.find_all('span', class_='visually-hidden')
#
#                         for i in Education_local:
#                             data1 = i.get_text().strip()
#                             data1 = data1.replace('\n\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n', '\n')
#                             data1 = data1.replace('\n\n', '\n')
#                             EducationList.append(data1)
#                         Education = '\n'.join(map(str, EducationList))
#                         EducationList.clear()
#                 elif 'SkillsSkills' in data:
#                     skillsSource = data_source
#                     SkillsList = []
#                     if 'Show all' in data:
#                         local = skillsSource.find('div', class_="pvs-list__footer-wrapper")
#                         geturl = local.find('a')['href']
#                         driver.get(geturl)
#                         sleep(2)
#                         Skills_local = driver.find_element_by_xpath('//*[@class="artdeco-card ember-view pb3"]')
#                         Skills_locals = Skills_local.find_elements_by_xpath('//*[@class="visually-hidden"]')
#
#                         for i in Skills_locals:
#                             data1 = i.get_text().strip()
#                             data1 = data1.replace('\n\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n', '\n')
#                             data1 = data1.replace('\n\n', '\n')
#                             SkillsList.append(data1)
#                         Skills = '\n'.join(map(str, SkillsList))
#                         SkillsList.clear()
#                         pass
#                     else:
#                         Skills_local = skillsSource.find_all('span',class_='visually-hidden')
#                         for i in Skills_local:
#                             data1 = i.get_text().strip()
#                             data1 = data1.replace('\n\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n', '\n')
#                             data1 = data1.replace('\n\n', '\n')
#                             SkillsList.append(data1)
#                         Skills = '\n'.join(map(str, SkillsList))
#                         SkillsList.clear()
#
#                 elif 'LanguagesLanguages' in data:
#                     languagesSource = data_source
#                     LanguagesList = []
#                     if 'Show all' in data:
#
#                         local = skillsSource.find('div', class_="pvs-list__footer-wrapper")
#                         geturl = local.find('a')['href']
#                         driver.get(geturl)
#                         sleep(2)
#                         Languages_local = driver.find_element_by_xpath('//*[@class="artdeco-card ember-view pb3"]')
#                         Languages_locals = Languages_local.find_elements_by_xpath('//*[@class="visually-hidden"]')
#                         for i in Languages_locals:
#                             data1 = i.get_text().strip()
#                             data1 = data1.replace('\n\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n', '\n')
#                             data1 = data1.replace('\n\n', '\n')
#                             LanguagesList.append(data1)
#                         Languages = '\n'.join(map(str, LanguagesList))
#                         LanguagesList.clear()
#                         pass
#                     else:
#                         Languages_local = languagesSource.find_all('span', class_="visually-hidden")
#                         for i in Languages_local:
#                             data1 = i.get_text().strip()
#                             data1 = data1.replace('\n\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n\n', '\n')
#                             data1 = data1.replace('\n\n\n', '\n')
#                             data1 = data1.replace('\n\n', '\n')
#                             LanguagesList.append(data1)
#                         Languages = '\n'.join(map(str, LanguagesList))
#                         LanguagesList.clear()
#                 elif 'InterestsInterests' in data:
#                     interestsSource = data_source
#                     Interests_local = interestsSource.find_all('span', class_='visually-hidden')
#                     InterestsList = []
#                     for i in Interests_local:
#                         data1 = i.get_text().strip()
#                         data1 = data1.replace('\n\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n', '\n')
#                         data1 = data1.replace('\n\n', '\n')
#                         InterestsList.append(data1)
#                     Interests = '\n'.join(map(str, InterestsList))
#                     InterestsList.clear()
#                 elif 'RecommendationsRecommendations' in data:
#                     recommendationsSource = data_source
#                     Recommendations_local = recommendationsSource.find_all('span', class_="visually-hidden")
#                     RecommendationsList = []
#                     for i in Recommendations_local:
#                         data1 = i.get_text().strip()
#                         data1 = data1.replace('\n\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n', '\n')
#                         data1 = data1.replace('\n\n', '\n')
#                         RecommendationsList.append(data1)
#                     Recommendations = '\n'.join(map(str, RecommendationsList))
#                     RecommendationsList.clear()
#                     pass
#                 elif 'Licenses & certificationsLicenses & certifications' in data:
#                     licensesSource = data_source
#                     Licenses_local = licensesSource.find_all('span', class_="visually-hidden")
#                     LicensesList = []
#                     for i in LicensesList:
#                         data1 = i.get_text().strip()
#                         data1 = data1.replace('\n\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n', '\n')
#                         data1 = data1.replace('\n\n', '\n')
#                         LicensesList.append(data1)
#                     Licenses = '\n'.join(map(str, LicensesList))
#                     LicensesList.clear()
#                 elif 'EnglishEnglish' in data:
#                     certificationsSource = data_source
#                     Certifications_local = certificationsSource.find_all('span', class_="visually-hidden")
#                     CertificationsList = []
#                     for i in Certifications_local:
#                         data1 = i.get_text().strip()
#                         data1 = data1.replace('\n\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n', '\n')
#                         data1 = data1.replace('\n\n', '\n')
#                         CertificationsList.append(data1)
#                     Certifications = '\n'.join(map(str, CertificationsList))
#                     CertificationsList.clear()
#                 elif 'Honors & awardsHonors & awards' in data:
#                     awardsSource = data_source
#                     Awards_local = awardsSource.find_all('span', class_="visually-hidden")
#                     AwardsList = []
#                     for i in Awards_local:
#                         data1 = i.get_text().strip()
#                         data1 = data1.replace('\n\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n', '\n')
#                         data1 = data1.replace('\n\n', '\n')
#                         AwardsList.append(data1)
#                     Awards = '\n'.join(map(str, AwardsList))
#                     AwardsList.clear()
#                 elif 'OrganizationsOrganizations' in data:
#                     organizationsSource = data_source
#                     Organizations_local = organizationsSource.find_all('span', class_="visually-hidden")
#                     OrganizationsList = []
#                     for i in Organizations_local:
#                         data1 = i.get_text().strip()
#                         data1 = data1.replace('\n\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n\n', '\n')
#                         data1 = data1.replace('\n\n\n', '\n')
#                         data1 = data1.replace('\n\n', '\n')
#                         OrganizationsList.append(data1)
#                     Organizations = '\n'.join(map(str, OrganizationsList))
#                     OrganizationsList.clear()
#                 elif 'ActivityActivity' in data:
#                     activitySource = data_source
#                     Activity_local = activitySource.find_all('a',class_='app-aware-link feed-mini-update-optional-navigation-context-wrapper')
#                     ActivityList = []
#                     for i in Activity_local:
#                         data1 = i['href']
#                         data2 = {
#                             'url': data1
#                         }
#                         ActivityList.append(data2)
#                     #Activity1 = '\n'.join(map(str, ActivityList))
#                     Activity = json.dumps(ActivityList)
#                     ActivityList.clear()
#                 else:
#
#                     print(data)
#                     continue
#
#             # contact
#             #Contact =
#             driver.find_element_by_xpath('//*[@id="top-card-text-details-contact-info"]').click()
#             sleep(3)
#             data3 = driver.find_element_by_xpath('//*[@class="pv-profile-section__section-info section-info"]').text
#             print(data3)
#             data3 = data3.replace('\n\n', '')
#             data3 = data3.replace('  ', '')
#             data3 = data3.replace('\n\n', '\n')
#             Contact = data3
#
#             Licenses = Licenses + '\n' + Certifications
#             writer.writerow(
#                 {headers[0]: linkedin_URL, headers[1]: Name, headers[2]: Contact, headers[3]: Location, headers[4]: Current_Job,
#                  headers[5]: About, headers[6]: Experience, headers[7]: Education, headers[8]: Skills, headers[9]: Languages,
#                  headers[10]: Interests, headers[11]: Licenses,headers[12]: Recommendations,headers[13]: Awards,headers[14]: Organizations,
#                  headers[15]: Activity})
#             print('\n')
#             jsondata = {
#                 'ProfileUrl':Linkedin,
#                 'Name':Name,
#                 'Contact':Contact,
#                 'Location':Location,
#                 'CurrentJob':Current_Job,
#                 'About':About,
#                 'Experience':Experience,
#                 'Education':Education,
#                 'Skill':Skills,
#                 'Languages':Languages,
#                 'Interests':Interests,
#                 'Licenses':Licenses,
#                 'Recommendation':Recommendations,
#                 'Award':Awards,
#                 'Organization':Organizations,
#                 'Activity':Activity,
#             }
#             print(jsondata)
#             url_upload = "http://localhost:6023/PythonCrawler/InsertLinkedinLog"
#             # url_upload = "https://dieuhanh.vatco.vn/PythonCrawler/InsertCrawlerRunningLog"
#             resp = requests.post(url_upload, data=jsondata)
#             if resp.ok:
#                 print("Upload completed successfully!")
#                 print("data report crawl!")
#                 print(resp.text)
#             else:
#                 print("Something went wrong!")
#         except:
#             print('cannot get data!')
#             pass


print('Mission Completed!')


