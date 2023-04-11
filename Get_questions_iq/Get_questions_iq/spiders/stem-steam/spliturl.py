import csv
import json
import pandas as pd
from tqdm import tqdm
import docx
header = ["link"]
selector1 = "2015/"
list_sec1 = []

with open(r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\stem-steam\url\stemsteamd7e07ea2-3bb5-4912-b586-b93ea1ac435e.csv', 'r') as f:
    csvreader = csv.reader(f)
    data = list(csvreader)
    for i in range(len(data)) :
        if 'docs.google'  in data[i][0] :
            list_sec1.append(data[i][0])

print(len(list_sec1))#hoa 1405


with open(r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\stem-steam\url\đocrive.csv', 'w', encoding='utf-8', newline ='') as outfile1:
    write = csv.writer(outfile1, delimiter='\n')
    write.writerow(header)
    write.writerow(list_sec1)
