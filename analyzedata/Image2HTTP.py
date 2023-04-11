import os
import requests

path = r'C:\Users\Administrator\Desktop\Image'
for root, dirs, files in os.walk(path):
    print(root)
    if 'images' in root or 'Source' in root:
        #print(root)
        dir_list = os.listdir(root)
        #print(dir_list)
        #print('---------------')
        print(len(dir_list))
        for value in dir_list:
            imagepath = root + '\\' +value
            print(value)

            print(imagepath)
            print('-------------------------')

            url = "https://dieuhanh.vatco.vn/MobileLogin/InsertObjectFileSubject"
            payload = {'ModuleName': 'SUBJECT',
                       'IsMore': 'false',
                       'CreatedBy': 'admin'}
            files = [
                ('fileUpload', (value, open(imagepath, 'rb'), 'image/png'))
            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            if response.ok:
                print("Upload completed successfully!")
                print(response.text)

            else:
                print("Something went wrong!")
                # writer.writerow({headers[0]: LinkUrl})



