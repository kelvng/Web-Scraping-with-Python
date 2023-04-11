import uuid
import shortuuid
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import qrcode

# obj_qr = qrcode.QRCode(
#     version = 1,
#     error_correction = qrcode.constants.ERROR_CORRECT_L,
#     box_size = 10,
#     border = 4,
# )
link = ['https://tuyendung.topcv.vn/app/cvs-management/cvs/13570391?share-token=eyJ0b2tlbl9uYW1lIjoiZW1wbG95ZXJfY3ZfbWFuYWdlbWVudF90b2tlbiIsImV4cGlyZWRfYXQiOiIyMDIyLTExLTEzIDEwOjQ5OjA4In0.eyJlbXBsb3llcl9pZCI6OTQxMywiY3ZfcmVjb3JkX2lkIjoxMzU3MDM5MSwicm9sZV9uYW1lIjoiYW5vbnltb3VzIn0.9351818527a2179be7327127fe89be80',
       'https://tuyendung.topcv.vn/app/cvs-management/cvs/13569682?share-token=eyJ0b2tlbl9uYW1lIjoiZW1wbG95ZXJfY3ZfbWFuYWdlbWVudF90b2tlbiIsImV4cGlyZWRfYXQiOiIyMDIyLTExLTEzIDEwOjI5OjEzIn0.eyJlbXBsb3llcl9pZCI6OTQxMywiY3ZfcmVjb3JkX2lkIjoxMzU2OTY4Miwicm9sZV9uYW1lIjoiYW5vbnltb3VzIn0.5bcc149336525e52cda720c880ce1999',
       'https://tuyendung.topcv.vn/app/cvs-management/cvs/13569621?share-token=eyJ0b2tlbl9uYW1lIjoiZW1wbG95ZXJfY3ZfbWFuYWdlbWVudF90b2tlbiIsImV4cGlyZWRfYXQiOiIyMDIyLTExLTEzIDEwOjI3OjU3In0.eyJlbXBsb3llcl9pZCI6OTQxMywiY3ZfcmVjb3JkX2lkIjoxMzU2OTYyMSwicm9sZV9uYW1lIjoiYW5vbnltb3VzIn0.7f02d199280a426b0cede44582db0d24',
       'https://tuyendung.topcv.vn/app/cvs-management/cvs/13569529?share-token=eyJ0b2tlbl9uYW1lIjoiZW1wbG95ZXJfY3ZfbWFuYWdlbWVudF90b2tlbiIsImV4cGlyZWRfYXQiOiIyMDIyLTExLTEzIDEwOjI2OjA4In0.eyJlbXBsb3llcl9pZCI6OTQxMywiY3ZfcmVjb3JkX2lkIjoxMzU2OTUyOSwicm9sZV9uYW1lIjoiYW5vbnltb3VzIn0.c440cd42e0c855b8a0f733a5a3a0f92a&ref=mail']
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
browser = webdriver.Chrome(executable_path=r'F:\PycharmProjects\Source\chromedriver.exe',
                           options=options)
for i in link:
    browser.get(i)
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    Name = soup.find('div',class_="cv-name h6 mb-2 font-weight-bold").text.strip()
    MailObj = soup.find('div', class_="cv-contact mb-2")
    dataLst = MailObj.find_all('span')
    Mail  = dataLst[0].text
    phone = dataLst[2].text
    PdfLink = soup.find('a',class_="btn btn-secondary btn-lg btn-block")['href']
    print(Name)
    print(Mail)
    print(phone)
    print(PdfLink)
    print('-------------------------------------------')
    JsonTrick = {
        'Name': Name,
        'Email':Mail,
        'Phone':phone,
        'Pdf':PdfLink,
    }
    JsonTrick1 = json.dumps(JsonTrick)
    print(type(JsonTrick))
    myUUID = uuid.uuid4()
    UserName = str(myUUID)[:14].replace('-', '_')
    myUUID1 = shortuuid.uuid()
    password = str(myUUID1)[:8]
    DataQrcode = {
        'UserName': UserName,
        'Password': password,
    }
    DataQRCODE = json.dumps(DataQrcode)
    qr_img = qrcode.make(DataQRCODE)
    myUUID2 = shortuuid.uuid()
    Nameimg = str(myUUID1)
    Nameimg = Nameimg + '.jpg'
    path = r"F:\PycharmProjects\Source\CVParserModule\Image/" + Nameimg
    qr_img.save(path)

    url = "https://dieuhanh.vatco.vn/MobileLogin/InsertObjectFileSubject"
    payload = {'ModuleName': 'SUBJECT',
               'IsMore': 'false',
               'CreatedBy': 'admin'}
    files = [
        ('fileUpload', (Nameimg, open(path, 'rb'), 'image/png'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    if response.ok:
        #print("Upload completed successfully!")
        #print(response.text)
        IdData = json.loads(response.text)
        #print(IdData['Object'])
        IMG_DATE = IdData['Object'].replace('https://dieuhanh.vatco.vn', '')
    else:
        print("Something went wrong!")
        # writer.writerow({headers[0]: LinkUrl})
    data = {
        'UserName': UserName,
        'Password': password,
        'JsonData': JsonTrick1,
        'QrCode': IMG_DATE,
        'Status': False,
        'EmailCode': '',
    }
    url_upload = "http://localhost:6002/PythonCrawler/ReciveFromPy"
    resp = requests.post(url_upload, data=data)
    if resp.ok:
        print("Upload completed successfully!")
        print("data insert from Post!")
        print(resp.text)
    else:
        print("Something went wrong!")

browser.quit()

