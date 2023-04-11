import csv
import json
import pandas as pd
from tqdm import tqdm
import docx
header = ["link"]
selector1 = "luyen-tap"
selector2 = "trac-nghiem-vui"
selector3 = "vat-ly"
selector4 = "sinh-hoc"
selector5 = "tieng-anh"
selector6 = "dia-ly"
selector7 = "lich-su"
selector8 = "ngu-van"
selector9= "gdcd"
selector10="50-tinh-cach"
selector11 = "toan-hoc"
error_selec = "ket-qua"
selec = 'xac-nhan'
list_sec1 = []
list_sec2 = []
list_sec3 = []
list_sec4 = []
list_sec5 = []
list_sec6 = []
list_sec7 = []
list_sec8 = []
list_sec9 = []
list_sec10 = []
list_sec11 = []
with open(r'C:\Users\Admin\PycharmProjects\Source\koreacrawl\Korea_crawl\Korea_crawl\spiders\hoctiengkoreadeep_1.csv', 'r') as f:
    csvreader = csv.reader(f)
    data = list(csvreader)
    print(data[1][0])
    for i in range(len(data)):
        if selector1 in data[i][0] and error_selec not in data[i][0] and "download" not in data[i][0] and "lythuyet" not in data[i][0] and "chuong" not in data[i][0] and "chi-tiet" not in data[i][0] and "/level/" not in data[i][0]:
            list_sec1.append(data[i][0])
    for i in range(len(data)):
        if selector2 in data[i][0]:
            list_sec2.append(data[i][0])
print(len(list_sec1))#hoa 1405
print(len(list_sec2))#347

a = len(list_sec11) +len(list_sec1)+len(list_sec2)+len(list_sec3)+len(list_sec4)+len(list_sec5)+len(list_sec6)+len(list_sec7)+len(list_sec7) + len(list_sec9) + len(list_sec10)
print(a) #6821

with open('hoahoc.csv', 'w', encoding='utf-8', newline ='') as outfile1:
    write = csv.writer(outfile1, delimiter='\n')
    write.writerow(header)
    write.writerow(list_sec1)
with open(r'C:\Users\Admin\PycharmProjects\Source\koreacrawl\Korea_crawl\Korea_crawl\spiders'+'luyentap.csv', 'w', encoding='utf-8', newline ='') as outfile2:
    write = csv.writer(outfile2, delimiter='\n')
    write.writerow(header)
    write.writerow(list_sec2)
