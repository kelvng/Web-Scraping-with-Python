import csv
import os
import requests
import json
import time
from pathlib import Path
from glob import glob

import shutil
big_folder = input('Enter Big Folder: ')

target_folder = input('Enter target_folder: ')

CateRepoSettingId = int(input('enter CateRepoSettingId: '))

def getfileurl(path):
    url_upload = "https://dieuhanh.vatco.vn/MobileLogin/InsertFile"

    file_path = path
    filename = Path(file_path).name
    print(filename)
    print(file_path)
    old_path = os.path.dirname(os.path.abspath(file_path))
    response_upload = requests.post(url_upload, data={"CateRepoSettingId": CateRepoSettingId, "CreatedBy": "admin"},
                                    files={
                                        "fileUpload": (
                                            filename,
                                            open(file_path
                                                ,
                                                'rb'),
                                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    if response_upload.ok:
        print("Upload completed successfully!")
        print(response_upload.text)
        #print(File_Result)

        original = old_path + '\\'+filename
        target = target_folder + '\\' + filename

        #shutil.move(original, target)
        #os.remove(original)
    else:
        print("Something went wrong!")




for file in os.listdir(big_folder):
    path = os.path.join(big_folder, file)
    getfileurl(path)

    #2290