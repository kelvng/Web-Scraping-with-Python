import csv
import json
import pandas as pd
from tqdm import tqdm
import docx
header = ["link"]
selector1 = "thong-tin"
list_sec1 = []

with open(r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\loga2.csv', 'r') as f:
    csvreader = csv.reader(f)
    data = list(csvreader)
    print(data[1][0])
    for i in range(len(data)) :
        if selector1 not in data[i][0] :
            list_sec1.append(data[i][0])

print(len(list_sec1))#hoa 1405


with open(r'C:\Users\Admin 3i\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\loga\logaurl\loga2.csv', 'w', encoding='utf-8', newline ='') as outfile1:
    write = csv.writer(outfile1, delimiter='\n')
    write.writerow(header)
    write.writerow(list_sec1)
