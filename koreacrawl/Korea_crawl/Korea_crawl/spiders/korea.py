import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
#url ='https://hoctiengkorea.com/tu-vung/chu-de-am-nhac-hoi-hoa.html'
from tqdm import tqdm

#url = 'https://tuvungtienghan.com/xuat-khau-lao-dong/chi-tiet/tu-vung-tieng-han-trong-ngan-hang-2000-cau-hoi-phan-mot-326.html'
#quest url = ''
#
# products_data = pd.read_csv(
#     r'C:\Users\Admin\PycharmProjects\Source\koreacrawl\Korea_crawl\Korea_crawl\spiders\tracnghiemall.csv')
# list_link = tqdm(products_data['link'].tolist())
#
# for link in list_link:
#     req = requests.get(link)
#     data = req.text
#     soup = BeautifulSoup(data, 'lxml')
#
#     local = soup.find('div', class_= "row")
#     question = local.find_all('div', class_="col-xs-12 col-sm-6 col-md-6 col-lg-6 padding")
#     lst =[]
#
#     data2 ={
#     "exam":  lst
#     }
#     json_string = json.dumps(data2, indent= 4)
#     print(json_string)
#     with open(r'C:\Users\Admin\PycharmProjects\Source\koreacrawl\Korea_crawl\Korea_crawl\spiders' + 'korea.json', 'w') as f:
#     #f.write(json_string)
s = '③ 오염'
x = '④ 조절'

y = 'Sai. Rất tiếc đáp án phải là ③ 오염'
if x in y :
    print("true")

else:
    print('False')

