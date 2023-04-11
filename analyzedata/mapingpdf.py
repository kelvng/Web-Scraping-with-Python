import csv
import os
import shutil

import requests
import json
import time
from pathlib import Path
from glob import glob
error = []
target_folder = input('Enter target_folder: ')
def getfileurl(path):
    url_upload = "https://dieuhanh.vatco.vn/MobileLogin/InsertFile"
    file_path = path
    filename = Path(file_path).name
    old_path = os.path.dirname(os.path.abspath(file_path))
    response_upload = requests.post(url_upload, data={"CateRepoSettingId": 2247, "CreatedBy": "huynv_cntt_3i"},
                                    files={
                                        "fileUpload": (
                                            filename,
                                            open(file_path
                                                ,
                                                'rb'),
                                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    if response_upload.ok:
        print("Upload completed successfully!")
        #print(response_upload.text)

        statusupload=response_upload.text
        datasend = json.loads(statusupload)
        File_Result = datasend['Object']["Url"]
        print(File_Result)
        # original = old_path + '\\' + filename
        # target = target_folder + '\\' + filename
        #
        # shutil.move(original, target)

        return  File_Result
    else:
        print("Something went wrong!")
        error.append(path)
filepath = r'D:\wwwroot\Crawler data\14-12\Vaatl ý 10'
pathsub = glob(filepath+ '\*', recursive = True)
# print(len(pathsub))
for i in pathsub:
    print(i)
    filelst = os.listdir(i)
    fileurl = ''
    for j in filelst:
        if j.endswith(".pdf") or j.endswith(".doc")  or j.endswith(".docx"):
            fileurl = getfileurl(i + "\\" + j)
            print(fileurl)
            ## load to API

    if 'https://dieuhanh' in fileurl:
        for h in filelst:
            if h.endswith(".json"):
                path = i + '\\' + h
                f = open(path)

                data = json.load(f)

                data["FilePath"] = fileurl
                #print(data)
                with open(i + '\\' + h, 'w') as fp:
                    json.dump(data, fp, indent=4)
    else:
        print("API lỗi!")



with open(filepath + '/' + 'LISTFAILE_FAIL.csv', 'w', newline='', encoding="utf-8") as file_output:
    headers = ['PROFILEURL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
    writer.writeheader()
    for i in error:
        LinkUrl = i
        writer.writerow({headers[0]: LinkUrl})

