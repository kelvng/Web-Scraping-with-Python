import requests
from bs4 import BeautifulSoup
url = 'https://www.proprofs.com/quiz-school/topic/software-testing'
req = requests.get(url)
page_source = req.text
soup = BeautifulSoup(page_source,'lxml')
link = soup.find('div',class_='left_wrapper dleftwrapperpp')
for i in link.find_all('a'):

    print('https://www.proprofs.com' + i['href'])
