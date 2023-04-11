import requests

url_upload = "http://localhost:6002/MobileLogin/InsertCategory1"
catcode = 'LMS_KHTN_5'
catname ='Môn Khoa học tự nhiên lớp 5'
catparent = 'LMS_KHTN_MAIN'

foldername = 'LMS-KHTN-MAIN'
path = '/LMS_DOCUMENTS/LMS-KHTN-MAIN'

param = {
    "ReposCode": "02",
    "TypeRepos":"SERVER",


    "CatCode": catcode,
    "CatName": catname,
    "CatParent": catparent,
    "IsDeleted": False,
    "ModuleFileUploadDefault": "",
    "Id": 0,
    "CreatedBy": "admin",
    "FolderId":"",
    "FolderName":foldername,
    "Path": path,
}
print(param)
response_upload = requests.post(url_upload,data = param)

if response_upload.ok:
    print("Upload completed successfully!")
    print(response_upload.text)
else:
    print("Something went wrong!")
