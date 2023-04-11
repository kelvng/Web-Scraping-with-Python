# coding=utf8
# -*- coding: utf-8 -*-
import csv
from time import sleep
import uuid
import json
from docx import Document
import glob
import os
document = Document(r'\\QUARK6\DataCrawler\Thuvienhoclieu.com\.GDCD\Lớp 6\queiz\thuvienhoclieu.com-Trac-Nghiem-GDCD-6-Bai-8.docx')
fulltexxt = []
quizz = []
TF =[]
for para in document.paragraphs:

    if 'Câu' in para.text:
        quizz.append(para.text)
    elif 'ĐÁP ÁN:' in para.text:
        TF.append(para.text)
    else:

        fulltexxt.append(para.text)


print(quizz)
print(TF)
print(fulltexxt)
data_sample = ' '.join(map(str,fulltexxt))
print(data_sample)

data = data_sample.split('A.')

del data[0]
for i in data:
    data2 = i.split('B.')
    print(data2)
    for j in data2:
        data3 = j.split('C.')
        print(data3)
        for g in data3:
            data4 = j.split('D.')
            print(data4)
