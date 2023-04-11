# data get from server send

''' {"Url":"https://vneconomy.vn/","BotCode":"vneconomy-004","ListKeyWord":"[\"Dow Jones\",\"USD\",\"Covid\"]","DataStoragePath":"https/117.6.131.222/crawlerdate/cv1.html","DeepScan":2,"IsDownloadFile":true,"ConfigSelectorJson":"{\"header\": \"header\", \"headerclass\": \"detail__header\", \"content\": \"div\", \"contentclass\": \"detail__content\", \"image\": \"figure\", \"imageclass\": \"{'class':['detail__avatar', 'image-wrap align-center-image']}\"}"}'''

# json.loads
'''{'Url': 'https://vneconomy.vn/', 'BotCode': 'vneconomy-004', 'ListKeyWord': "['Dow Jones','USD','Covid']", 'DataStoragePath': 'https/117.6.131.222/crawlerdate/cv1.html', 'DeepScan': 2, 'IsDownloadFile': True, 'ConfigSelectorJson': "{'header': 'header', 'headerclass': 'detail__header', 'content': 'div', 'contentclass': 'detail__content', 'image': 'figure', 'imageclass': 'class':['detail__avatar', 'image-wrap align-center-image']}'}"}'''

#jsonfomat
'''{
    "Url": "https://vneconomy.vn/",
    "BotCode": "vneconomy-004",
    "ListKeyWord": "['Dow Jones','USD','Covid']",
    "DataStoragePath": "https/117.6.131.222/crawlerdate/cv1.html",
    "DeepScan": 2,
    "IsDownloadFile": true,
    "ConfigSelectorJson": "{'header': 'header', 'headerclass': 'detail__header', 'content': 'div', 'contentclass': 'detail__content', 'image': 'figure', 'imageclass': 'class':['detail__avatar', 'image-wrap align-center-image']}'}"
}'''