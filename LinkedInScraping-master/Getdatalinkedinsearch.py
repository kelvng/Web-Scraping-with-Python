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
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
print('- Finish importing packages')

# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path=r'F:\PycharmProjects\Source\chromedriver.exe',
                          options=options)

url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

# Task 1.2: Import username and password

credential = open(r'F:\PycharmProjects\Source\LinkedInScraping-master\credential\credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
print('- Finish importing the login credentials')

# https://www.linkedin.com/search/results/people/?geoUrn=%5B%22104195383%22%2C%2290010187%22%2C%2290010186%22%2C%22103697962%22%2C%22100921423%22%5D&network=%5B%22F%22%2C%22S%22%5D&origin=FACETED_SEARCH&page=100&sid=.nH
# Task 1.2: Key in login credentials
email_field = driver.find_element_by_id('username')
email_field.send_keys(username)
print('- Finish keying in email')
sleep(1.5)

password_field = driver.find_element_by_name('session_password')
password_field.send_keys(password)
print('- Finish keying in password')
sleep(1.5)
# Task 1.2: Click the Login button
signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()


print('- Finish Task 1: Login to Linkedin')
keyword_find = input('search People with keyword : ')
print('- Search match UID From DB')
#Diplomatic Academy of Vietnam
#keyword_find = keyword_find.replace(' ','%20')
# http://117.6.131.222:8989/PythonCrawler/GetLinkedInProfile?input=Diplomatic%20Academy%20of%2Vietnam
# vietnam
url_upload = 'http://117.6.131.222:8989/PythonCrawler/GetLinkedInProfile?input=' + keyword_find
#url_upload = 'http://localhost:8988/PythonCrawler/GetLinkedInProfile?input=vietnam'
response = requests.request("POST", url_upload)

element_data = json.loads(response.text)
print(type(element_data))

dem = 0
checklengt = 0
#element_data1 = ['https://www.linkedin.com/in/thang-cao-269979177/','https://www.linkedin.com/in/phan-duy-duong-a180a372/']
for datalinkedin in tqdm(element_data):
    print('------------------------------------------------------------------')
    ProfileUrl = datalinkedin['ProfileId']
    KeyWord = datalinkedin['KeyWord']
    print(KeyWord)

    driver.get(ProfileUrl)
    delay = 3  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print("Page is ready!")

    except TimeoutException:
        print("Loading took too much time!")

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    info_div = soup.find('body')
    #try:
    Email = ''
    Phone = ''
    About = ''
    Experience = ''
    Education = ''
    Skills = ''
    Languages = ''
    Interests = ''
    Licenses = ''
    Recommendations = ''
    Awards = ''
    Organizations = ''
    Certifications = ''
    Activity = ''

    info_div = info_div.find('main', class_='scaffold-layout__main')

    Name = info_div.find('h1',
                         class_="text-heading-xlarge inline t-24 v-align-middle break-words").get_text().strip()  # Remove unnecessary characters
    print('--- Profile name is: ', Name)
    Location = info_div.find('span',
                             class_='text-body-small inline t-black--light break-words').get_text().strip()  # Remove unnecessary characters
    print('--- Profile location is: ', Location)
    Current_Job = info_div.find('div', class_='text-body-medium break-words').get_text().strip()
    print('--- Job location is: ', Current_Job)
    # all ifo finding
    skillList = info_div.find_all('section', class_='artdeco-card ember-view relative break-words pb3 mt2')
    # profile url
    Linkedin = driver.current_url
    print('- Accessing profile: ', Linkedin)
    # contact
    # Contact =

    contactUrl = Linkedin  + '/overlay/contact-info/'
    driver.get(contactUrl)
    delay = 7  # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="pv-profile-section__section-info section-info"]')))
        print("Page is ready!")

    except TimeoutException:
        print("Loading took too much time!")

    data3 = driver.find_element_by_xpath('//*[@class="pv-profile-section__section-info section-info"]').text

    data3 = data3.replace('\n\n', '')
    data3 = data3.replace('  ', '')
    data3 = data3.replace('\n\n', '\n')
    Contact = data3
    print('Contact Info: ' + Contact)
    data_mail = ''
    data_phone = ''
    email_local = Contact.split('\n')
    for i in range(len(email_local)):
        if email_local[i] == 'Email':
            data_mail = email_local[i + 1]
            break
    for i in range(len(email_local)):
        if email_local[i] == 'Phone':
            data_phone = email_local[i+1]
            break
    Email = data_mail
    Phone = data_phone
    # print('--- list is : ', skillList)

    Linkedin = Linkedin
    for i in skillList:
        data_source = i
        data = data_source.get_text().strip()
        # print(data_source.get_text().strip())
        # print('------------------------------------------------------')
        # stirng = '---------------------------------------------------------'
        data = data.replace('\n\n\n\n\n', '\n')
        data = data.replace('\n\n\n\n', '\n')
        data = data.replace('\n\n\n', '\n')
        data = data.replace('\n\n', '\n')
        if 'AboutAbout' in data:
            aboutSource = data_source
            About_local = aboutSource.find_all('span', class_="visually-hidden")
            AboutList = []
            for i in About_local:
                data1 = i.get_text().strip()
                data1 = data1.replace('\n\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n', '\n')
                data1 = data1.replace('\n\n', '\n')
                About = data1
            # artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column
        elif 'ExperienceExperience' in data:
            experienceSource = data_source
            ExperienceList = []
            if 'Show all' in data:
                local = experienceSource.find('div', class_="pvs-list__footer-wrapper")
                geturl = local.find('a')['href']
                driver.get(geturl)
                delay = 5  # seconds
                try:
                    myElem = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@class="artdeco-card ember-view pb3"]')))
                    print("Page is ready!")

                except TimeoutException:
                    print("Loading took too much time!")

                Experience_local = driver.find_element_by_xpath('//*[@class="artdeco-card ember-view pb3"]')
                Experience_locals = Experience_local.find_elements_by_xpath('//*[@class="visually-hidden"]')
                for i in Experience_locals:
                    data1 = i.text.strip()
                    data1 = data1.replace('\n\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n', '\n')
                    data1 = data1.replace('\n\n', '\n')
                    ExperienceList.append(data1)
                Experience = '\n'.join(map(str, ExperienceList))
                ExperienceList.clear()
                pass
            else:

                # Experience_local = experienceSource.find_all('li',class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")
                Experience_local = experienceSource.find_all('span', class_='visually-hidden')

                for i in Experience_local:
                    data1 = i.get_text().strip()
                    data1 = data1.replace('\n\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n', '\n')
                    data1 = data1.replace('\n\n', '\n')
                    ExperienceList.append(data1)
                Experience = '\n'.join(map(str, ExperienceList))
                ExperienceList.clear()

        elif 'EducationEducation' in data:
            educationSource = data_source
            EducationList = []
            if 'Show all' in data:
                local = educationSource.find('div', class_="pvs-list__footer-wrapper")
                geturl = local.find('a')['href']
                driver.get(geturl)
                delay = 3  # seconds
                try:
                    myElem = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@class="artdeco-card ember-view pb3"]')))
                    print("Page is ready!")

                except TimeoutException:
                    print("Loading took too much time!")

                Education_local = driver.find_element_by_xpath('//*[@class="artdeco-card ember-view pb3"]')
                Education_locals = Education_local.find_elements_by_xpath('//*[@class="visually-hidden"]')
                for i in Education_locals:
                    data1 = i.text.strip()
                    data1 = data1.replace('\n\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n', '\n')
                    data1 = data1.replace('\n\n', '\n')
                    EducationList.append(data1)
                Education = '\n'.join(map(str, EducationList))
                EducationList.clear()
                pass
            else:

                # Education_local = educationSource.find_all('li',class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")
                Education_local = educationSource.find_all('span', class_='visually-hidden')

                for i in Education_local:
                    data1 = i.get_text().strip()
                    data1 = data1.replace('\n\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n', '\n')
                    data1 = data1.replace('\n\n', '\n')
                    EducationList.append(data1)
                Education = '\n'.join(map(str, EducationList))
                EducationList.clear()
        elif 'SkillsSkills' in data:
            skillsSource = data_source
            SkillsList = []
            if 'Show all' in data:
                local = skillsSource.find('div', class_="pvs-list__footer-wrapper")
                geturl = local.find('a')['href']
                driver.get(geturl)
                delay = 7  # seconds
                try:
                    myElem = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@class="artdeco-card ember-view pb3"]')))
                    print("Page is ready!")

                except TimeoutException:
                    print("Loading took too much time!")

                Skills_local = driver.find_element_by_xpath('//*[@class="artdeco-card ember-view pb3"]')
                Skills_locals = Skills_local.find_elements_by_xpath('//*[@class="visually-hidden"]')

                for i in Skills_locals:
                    data1 = i.text.strip()
                    data1 = data1.replace('\n\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n', '\n')
                    data1 = data1.replace('\n\n', '\n')
                    SkillsList.append(data1)
                Skills = '\n'.join(map(str, SkillsList))
                SkillsList.clear()
                pass
            else:
                Skills_local = skillsSource.find_all('span', class_='visually-hidden')
                for i in Skills_local:
                    data1 = i.get_text().strip()
                    data1 = data1.replace('\n\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n', '\n')
                    data1 = data1.replace('\n\n', '\n')
                    SkillsList.append(data1)
                Skills = '\n'.join(map(str, SkillsList))
                SkillsList.clear()

        elif 'LanguagesLanguages' in data:
            languagesSource = data_source
            LanguagesList = []
            if 'Show all' in data:

                local = languagesSource.find('div', class_="pvs-list__footer-wrapper")
                geturl = local.find('a')['href']
                driver.get(geturl)
                delay = 3  # seconds
                try:
                    myElem = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
                    print("Page is ready!")

                except TimeoutException:
                    print("Loading took too much time!")

                Languages_local = driver.find_element_by_xpath('//*[@class="artdeco-card ember-view pb3"]')
                Languages_locals = Languages_local.find_elements_by_xpath('//*[@class="visually-hidden"]')
                for i in Languages_locals:
                    data1 = i.text.strip()
                    data1 = data1.replace('\n\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n', '\n')
                    data1 = data1.replace('\n\n', '\n')
                    LanguagesList.append(data1)
                Languages = '\n'.join(map(str, LanguagesList))
                LanguagesList.clear()
                pass
            else:
                Languages_local = languagesSource.find_all('span', class_="visually-hidden")
                for i in Languages_local:
                    data1 = i.get_text().strip()
                    data1 = data1.replace('\n\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n\n', '\n')
                    data1 = data1.replace('\n\n\n', '\n')
                    data1 = data1.replace('\n\n', '\n')
                    LanguagesList.append(data1)
                Languages = '\n'.join(map(str, LanguagesList))
                LanguagesList.clear()
        elif 'InterestsInterests' in data:
            interestsSource = data_source
            Interests_local = interestsSource.find_all('span', class_='visually-hidden')
            InterestsList = []
            for i in Interests_local:
                data1 = i.get_text().strip()
                data1 = data1.replace('\n\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n', '\n')
                data1 = data1.replace('\n\n', '\n')
                InterestsList.append(data1)
            Interests = '\n'.join(map(str, InterestsList))
            InterestsList.clear()
        elif 'RecommendationsRecommendations' in data:
            recommendationsSource = data_source
            Recommendations_local = recommendationsSource.find_all('span', class_="visually-hidden")
            RecommendationsList = []
            for i in Recommendations_local:
                data1 = i.get_text().strip()
                data1 = data1.replace('\n\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n', '\n')
                data1 = data1.replace('\n\n', '\n')
                RecommendationsList.append(data1)
            Recommendations = '\n'.join(map(str, RecommendationsList))
            RecommendationsList.clear()
            pass
        elif 'Licenses & certificationsLicenses & certifications' in data:
            licensesSource = data_source
            Licenses_local = licensesSource.find_all('span', class_="visually-hidden")
            LicensesList = []
            for i in LicensesList:
                data1 = i.get_text().strip()
                data1 = data1.replace('\n\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n', '\n')
                data1 = data1.replace('\n\n', '\n')
                LicensesList.append(data1)
            Licenses = '\n'.join(map(str, LicensesList))
            LicensesList.clear()
        elif 'EnglishEnglish' in data:
            certificationsSource = data_source
            Certifications_local = certificationsSource.find_all('span', class_="visually-hidden")
            CertificationsList = []
            for i in Certifications_local:
                data1 = i.get_text().strip()
                data1 = data1.replace('\n\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n', '\n')
                data1 = data1.replace('\n\n', '\n')
                CertificationsList.append(data1)
            Certifications = '\n'.join(map(str, CertificationsList))
            CertificationsList.clear()
        elif 'Honors & awardsHonors & awards' in data:
            awardsSource = data_source
            Awards_local = awardsSource.find_all('span', class_="visually-hidden")
            AwardsList = []
            for i in Awards_local:
                data1 = i.get_text().strip()
                data1 = data1.replace('\n\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n', '\n')
                data1 = data1.replace('\n\n', '\n')
                AwardsList.append(data1)
            Awards = '\n'.join(map(str, AwardsList))
            AwardsList.clear()
        elif 'OrganizationsOrganizations' in data:
            organizationsSource = data_source
            Organizations_local = organizationsSource.find_all('span', class_="visually-hidden")
            OrganizationsList = []
            for i in Organizations_local:
                data1 = i.get_text().strip()
                data1 = data1.replace('\n\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n\n', '\n')
                data1 = data1.replace('\n\n\n', '\n')
                data1 = data1.replace('\n\n', '\n')
                OrganizationsList.append(data1)
            Organizations = '\n'.join(map(str, OrganizationsList))
            OrganizationsList.clear()
        elif 'ActivityActivity' in data:
            activitySource = data_source
            Activity_local = activitySource.find_all('a',
                                                     class_='app-aware-link feed-mini-update-optional-navigation-context-wrapper')
            ActivityList = []
            for i in Activity_local:
                data1 = i['href']
                data2 = {
                    'url': data1
                }
                ActivityList.append(data2)
            # Activity1 = '\n'.join(map(str, ActivityList))
            Activity = json.dumps(ActivityList)
            ActivityList.clear()
        else:
            print(data)
            continue

    Licenses = Licenses + '\n' + Certifications
    print('\n')
    jsondata = {
        'ProfileUrl': Linkedin,
        'Name': Name,
        'Contact': Contact,
        'Location': Location,
        'CurrentJob': Current_Job,
        'About': About,
        'Experience': Experience,
        'Education': Education,
        'Skill': Skills,
        'Languages': Languages,
        'Interests': Interests,
        'Licenses': Licenses,
        'Recommendation': Recommendations,
        'Award': Awards,
        'Organization': Organizations,
        'Activity': Activity,
        'ElementSite':KeyWord,
        'Email': Email,
        'Phone': Phone,
    }
    print(jsondata)
    url_upload = "http://117.6.131.222:8989/PythonCrawler/InsertLinkedInInfo"
    # url_upload = "https://dieuhanh.vatco.vn/PythonCrawler/InsertCrawlerRunningLog"
    resp = requests.post(url_upload, data=jsondata)
    if resp.ok:
        print("Upload completed successfully!")
        print("data report crawl!")
        print(resp.text)
    else:
        print("Something went wrong!")


