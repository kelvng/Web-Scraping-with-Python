# import json
# from os import listdir
# from os.path import isfile, join
# path = r'D:\PycharmProjects\Json\CNTTDONE\phần cứng máy tính'
# onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
# print(onlyfiles)
# dem = 0
# for i in onlyfiles:
#     path_file = path + '\\' + i
#     print(path_file)
#     with open(path_file, 'r') as data:
#         y = json.load(data)
#     dem = dem +1
#     print(y["ExamName"])
#     y["ExamName"] = "Đề số " + str(dem) + " trắc nghiệm phần cứng máy tính"
#     print(y["ExamName"])
#
#     json_string = json.dumps(y, indent= 4)
#     with open(path_file, "w") as f:
#         f.write(json_string)

import json
import os
from os import listdir
from os.path import isfile, join

path = r'D:\PycharmProjects\Json\update\y té'

list = os.walk(path)
print(list)
list_path = [x[0] for x in os.walk(path)]
print(list_path)
for i in range(len(list_path)):
    path = list_path[i]
    if i == 0:
        continue
    else:
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        #print(onlyfiles)

        dem = 0
        for i in onlyfiles:
            path_file = path + '\\' + i
            #print(path_file)
            with open(path_file, 'r') as data:
                y = json.load(data)
            dem = dem +1
            examname = y["ExamName"]
            print(examname)
            if 'Trắc nghiệm' in examname:

                mainstring = examname.split('Trắc nghiệm')
            elif 'trắc nghiệm' in examname:
                mainstring = examname.split('trắc nghiệm')
            print(mainstring)
            mainstring = mainstring[1]

            y["ExamName"] = "Đề số " + str(dem) + mainstring
            print(y["ExamName"])

            json_string = json.dumps(y, indent= 4)
            with open(path_file, "w") as f:
                f.write(json_string)

# import requests
# from PIL import ImageFile
# url = 'https://s.tracnghiem.net/images/tests/2021/20210208//thumbnail/230x144/216_1613614458.jpg'
# resume_header = {'Range': 'bytes=0-2000000'}    ## the amount of bytes you will download
# data = requests.get(url, stream = True, headers = resume_header).content
#
# p = ImageFile.Parser()
# p.feed(data)    ## feed the data to image parser to get photo info from data headers
# if p.image:
#     print(p.image.size) ## get the image size (Width, Height)
#
# ## output: (1400, 1536)
