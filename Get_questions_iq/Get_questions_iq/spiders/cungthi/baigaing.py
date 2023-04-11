
import json
import os
import re
import sys
import uuid
from datetime import datetime
from time import sleep
from docx import Document
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_baigiangcungthi():
    link = 'https://cungthi.online/bai-giang/toan-hoc/lop-12/bai-giang-mon-toan-lop-12-phan-hinh-hoc-chuyen-de-khoi-da-dien-goc-va-khoang-cach.html'

    data = {
        "ID": 0,
        "SubjectName": "",
        "Title": "",
        "ExamName": "",
        "Source": "",
        "Error": False,
        "Object": {
            "isAlreadyDone": False,
            "details": ""
        },
        "Code": "uuid"
    }
    req = requests.get(link, verify=False)
    sleep(1)
    page_source = req.text
    soup = BeautifulSoup(page_source, 'html.parser')
    subjectname = soup.find('h2').text.replace("  ","")
    type = soup.find('li',class_="active").text.replace("   ","")
    title = soup.find('h1', class_="h1_rewrite").text.replace("   ","")
    data['SubjectName'] = subjectname
    data['ExamName'] = type
    data['Title'] = title
    print(type)
    print(title)
    print(subjectname)

    local = soup.find('div', class_="col-md-9")
    local_lecture = local.find('ul')
    link_lecture = local_lecture.find_all('a')
    list_lecture = []
    for j in link_lecture:
        name_lecture = j.text
        link_lecture = j['href']
        req = requests.get(link_lecture, verify=False)
        sleep(1)
        page_source = req.text
        soup = BeautifulSoup(page_source, 'html.parser')
        local1 = soup.find('div', class_="col-md-9")
        local_lecture1 = local1.find_all('p')
        data_lecture = ' '.join(map(str, local_lecture1))

        quest = {
                "Id": 1,
                "LECT_NAME": "",
                "Content": "",
                "Code": "9c4eeac2-2ed5-42db-8980-d9b6003c972b",
                "Type": "LECTURE",
                }
        quest['Content'] = data_lecture
        quest['LECT_NAME'] = name_lecture

        list_lecture.append(quest)
        # list_lecture.append(name_lecture)
        # list_lecture.append(link_lecture)
        # list_lecture.append(data_lecture)
    dict2 = {
        "ID": 0,
        "SubjectName": subjectname,
        "Title": title,
        "ExamName": type,
        "Error": False,
        "Object": {
            "isAlreadyDone": False,
            "details": list_lecture
        },
        "Code": "uuid"
    }
    data_string = json.dumps(dict2, indent=4)


    with open("hell.json", "w") as f:
        f.write(data_string)


get_baigiangcungthi()
