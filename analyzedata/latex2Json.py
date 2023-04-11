# coding=utf8
# -*- coding: utf-8 -*-
import csv
from time import sleep
import uuid
import json

import requests
from docx import Document
import glob
from pathlib import Path
import os
big_folder = input('Enter Big Folder: ')
subject_name = input('enter subject: ')
Title_name = input('enter title: ')




def getfileurl(path):
    url_upload = "https://dieuhanh.vatco.vn/MobileLogin/InsertFile"
    file_path = path
    filename = Path(file_path).name
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
        #print(File_Result)
        return  File_Result
    else:
        print("Something went wrong!")

#data from json
json_data = {
    "ID": None,
    "SubjectName": "",
    "Title": "",
    "ExamName": "",
    "Error": False,
    "Object": {
        "isAlreadyDone": False,
        "details": []
    },
    "Code": "",
    "FilePath":"",
}
Json_Data = {
                "Id": 1,
                "Order": "",
                "Duration": 10,
                "Unit": "MINUTE",
                "Mark": 10,
                "Content": "",
                "Solve": {
                    "Solver": "Solve Quest",
                    "SolveMedia": [
                        {
                            "Code": "VIDEO",
                            "Name": "Video",
                            "Icon": "play",
                            "Url": "",
                            "Check": False
                        },
                        {
                            "Code": "IMAGE",
                            "Name": "Image",
                            "Icon": "image",
                            "Url": "title_img",
                            "Check": False
                        },
                        {
                            "Code": "VOICE",
                            "Name": "Voice",
                            "Icon": "microphone-alt",
                            "Url": "",
                            "Check": False
                        }
                    ]
                },
                "QuestionMedia": [
                    {
                        "Code": "VIDEO",
                        "Name": "Video",
                        "Icon": "play",
                        "Url": "",
                        "Check": False,
                        "$$hashKey": "object:55"
                    },
                    {
                        "Code": "IMAGE",
                        "Name": "Image",
                        "Icon": "image",
                        "Url": "",
                        "Check": False,
                        "$$hashKey": "object:56"
                    },
                    {
                        "Code": "VOICE",
                        "Name": "Voice",
                        "Icon": "microphone-alt",
                        "Url": "",
                        "Check": False,
                        "$$hashKey": "object:57"
                    }
                ],
                "Code": "6db14a5f-9062-457c-b591-d4b1a80bf45c",
                "Type": "QUIZ_SING_CH",
                "AnswerData": [
                    {
                        "Code": "925849e8-1778-4400-99e2-9fc2f6ab0df3",
                        "Answer": "",
                        "Type": "TEXT",
                        "ContentDecode": "",
                        "IsAnswer": False
                    },
                    {
                        "Code": "6fc0fb89-d246-48fb-bf66-adca0287276e",
                        "Answer": "",
                        "Type": "TEXT",
                        "ContentDecode": "",
                        "IsAnswer": False
                    },
                    {
                        "Code": "0fb98fc7-dc59-45de-a617-be1e6834198e",
                        "Answer": "",
                        "Type": "TEXT",
                        "ContentDecode": "",
                        "IsAnswer": False
                    },
                    {
                        "Code": "35b3b228-45c2-404d-888d-155c88eaf5b5",
                        "Answer": "",
                        "Type": "TEXT",
                        "ContentDecode": "",
                        "IsAnswer": False
                    }
                ],
                "IdQuiz": 75,
                "UserChoose": None
            }
fail_file = []
#parser latex\


fodlers = os.listdir(big_folder)
#print(fodlers)
for i in fodlers:
    #print(i)
    path_file = big_folder + '\\'+i
    path_file2 = big_folder + '\\' + i
    # files1 = glob.glob(path_file + '/*', recursive=True)
    # path_path = ''
    # for j in files1:
    #     if '.pdf' in j or '.doc' in j:
    #         print(j)
    #         path_path = getfileurl(j)
    #         print(path_path)
    # json_data['FilePath'] = path_path



    files = glob.glob(path_file+'/**/*.tex', recursive=True)
    #print(files)
    if files == []:
        continue
    else:
        Examname = i
        print(Examname)
        pass
    #sleep(1000)
    file1 = open(files[0], 'r', encoding= 'utf-8')
    #file1 = open(r'F:\PycharmProjects\Source\analyzedata\filedata\hello.tex', 'r', encoding='utf-8')
    Lines = file1.readlines()
    #print(Lines)
    value1 = ''
    for i in Lines:
        value1 = value1 + i
    numbquest =  value1 .split('\section{Đáp Án Đề}')
    #print(len(numbquest))
    #print(numbquest)
    del numbquest[0]
    for j in range(len(numbquest)):
        value = '\section{Đáp Án Đề}' + numbquest[j]
        #print(len(value.split("Câu")))
        quest =value.split("Câu")

        #print(quest)
        result = ''
        check = []
        #get list quest and list answer
        for h in quest:
            h = 'Câu' + h
            data1 = h.split('\n')
            if '\section{Đáp Án Đề}' in h:
                result = result + h
                #print('Đáp án: ' + result)
            else:
                for i in range(len(data1)):
                    data = data1[i]
                    if 'Câu' in data:
                        questask = data
                        #print('quest: ' + data) # Câu 1 >> true_text = 'B.'
                        check.append(data)
        #print(result.replace('\_','_').split('_'))
        if '_' in result:

            dataresult = result.replace('\_','_').split('_')
        elif '-' in result:
            dataresult = result.split('-')

        #parser get data from quizz
        Lst_QUIZZ = []
        del quest[0]
        #print(len(quest))

        #print(len(dataresult))

        print(str(len(dataresult)) + "Câu trả lờ")
        print(str(len(quest)) + "câu hỏi")
        if len(dataresult) == len(quest) :
            print('true way')
            Lst_ask = []
            for k in range(len(quest)):
                quest[k] = 'Câu' + quest[k]
                data1 = quest[k].split('\n')
                #print(data1)
                #print(data1)
                text_true = dataresult[k]
                #print('------------------------------------------------------------')
                text_true=text_true.replace('\n','')
                text_true = text_true.replace('\section{Đáp Án Đề}', '')
                #print(text_true)
                #print('---------------------------------')

                dataA = ''
                dataB = ''
                dataC = ''
                dataD = ''
                dataA_decode = ''
                dataB_decode = ''
                dataC_decode = ''
                dataD_decode = ''
                for i in range(len(data1)):
                    data = data1[i]
                    #print(data)
                    if 'A.' in data or '(A)' in data  or 'a.' in data or 'a)' in data  or 'A:' in data  or 'A-' in data or 'A)' in data and '$(A)$' not in data:

                        if '\includegraphics' in data:
                            data = data.replace('\\\\', '')
                            image = data.replace('\includegraphics', '')
                            image = image.replace('[max width=', '')
                            image = image.replace('textwidth]', '')
                            image = image.replace('\\', '')
                            image = image.replace('}', '')
                            image = image.replace('{', '')
                            image = image.replace('textwidth,', '')
                            image = image.replace('center],', '')
                            image = image.replace(' ', '')
                            #\includegraphics[max width=\textwidth]{yyNIACwR2tGNf--uTsHzhO3l6S0eHxo3IP9NFLNb4so_original_fullsize}
                            ##png or jpg
                            imgsource = '<img src="https://dieuhanh.vatco.vn//uploads/repository/SUBJECT/' + image + '.png'+ '" >'
                            data = imgsource
                            #print(data)
                            dataA_decode = data
                            #dataA = '<p>' + data + '</p>'
                            dataA = data
                            if 'A' in text_true:
                                Json_Data['AnswerData'][0]['IsAnswer'] = True
                            else:
                                Json_Data['AnswerData'][0]['IsAnswer'] = False
                        else:
                            data = data
                            dataA_decode = data
                            #dataA = '<p>' + data + '</p>'
                            dataA = data
                            if 'A' in text_true:
                                Json_Data['AnswerData'][0]['IsAnswer'] = True
                            else:
                                Json_Data['AnswerData'][0]['IsAnswer'] = False
                        # for char in char_remov:
                        #     # replace() "returns" an altered string
                        #     string = string.replace(char, "#")
                        # dataA = dataA.replace()
                    elif 'B.' in data or '(B)' in data or 'b.' in data or 'b)' in data  or 'B:' in data or 'B-' in data or 'B)' in data and '$(B)$' not in data:
                        if '\includegraphics' in data:
                            data = data.replace('\\\\', '')
                            image = data.replace('\includegraphics', '')
                            image = image.replace('[max width=', '')
                            image = image.replace('textwidth]', '')
                            image = image.replace('\\', '')
                            image = image.replace('}', '')
                            image = image.replace('{', '')
                            image = image.replace('textwidth,center]', '')
                            image = image.replace(' ', '')
                            imgsource = '<img src="https://dieuhanh.vatco.vn//uploads/repository/SUBJECT/' + image + '.png'+ '" >'
                            data = imgsource
                            dataB_decode = data
                            #dataB = '<p>' + data + '</p>'
                            dataB = data
                            if 'B' in text_true:
                                Json_Data['AnswerData'][1]['IsAnswer'] = True
                            else:
                                Json_Data['AnswerData'][1]['IsAnswer'] = False
                        else:
                            data = data
                            dataB_decode = data
                            #dataB = '<p>' + data + '</p>'
                            dataB = data
                            if 'B' in text_true:
                                Json_Data['AnswerData'][1]['IsAnswer'] = True
                            else:
                                Json_Data['AnswerData'][1]['IsAnswer'] = False

                    elif 'C.' in data or '(C)' in data or 'c.' in data or 'c)' in data or 'C:' in data or 'C-' in data or 'C)' in data and '$(C)$' not in data:
                        if '\includegraphics' in data:
                            data = data.replace('\\\\', '')
                            image = data.replace('\includegraphics', '')
                            image = image.replace('[max width=', '')
                            image = image.replace('textwidth]', '')
                            image = image.replace('\\', '')
                            image = image.replace('}', '')
                            image = image.replace('{', '')
                            image = image.replace('textwidth,center]', '')
                            image = image.replace(' ', '')
                            imgsource = '<img src="https://dieuhanh.vatco.vn//uploads/repository/SUBJECT/' + image + '.png'+ '" >'
                            data = imgsource

                            dataC_decode = data
                            dataC = data
                            if 'C' in text_true:
                                Json_Data['AnswerData'][2]['IsAnswer'] = True
                            else:
                                Json_Data['AnswerData'][2]['IsAnswer'] = False
                        else:
                            data = data
                            dataC_decode = data
                            #dataC = '<p>' + data + '</p>'
                            dataC = data
                            if 'C' in text_true:
                                Json_Data['AnswerData'][2]['IsAnswer'] = True
                            else:
                                Json_Data['AnswerData'][2]['IsAnswer'] = False

                    elif 'D.' in data or '(D)' in data or 'd.' in data or 'd)' in data or 'D:' in data or 'D-' in data or 'D)' in data and '$(D)$' not in data:
                        if '\includegraphics' in data:
                            data = data.replace('\\\\', '')
                            image = data.replace('\includegraphics', '')
                            image = image.replace('[max width=', '')
                            image = image.replace('textwidth]', '')
                            image = image.replace('\\', '')
                            image = image.replace('}', '')
                            image = image.replace('{', '')
                            image = image.replace('textwidth,center]', '')
                            image = image.replace(' ', '')
                            imgsource = '<img src="https://dieuhanh.vatco.vn//uploads/repository/SUBJECT/' + image + '.png'+ '" >'
                            data = imgsource
                            dataD_decode = data
                            #dataD = '<p>' + data + '</p>'
                            dataD = data
                            if 'D' in text_true:
                                Json_Data['AnswerData'][3]['IsAnswer'] = True
                            else:
                                Json_Data['AnswerData'][3]['IsAnswer'] = False
                        else:
                            data = data
                            dataD_decode = data
                            #dataD = '<p>' + data + '</p>'
                            dataD = data
                            if 'D' in text_true:
                                Json_Data['AnswerData'][3]['IsAnswer'] = True
                            else:
                                Json_Data['AnswerData'][3]['IsAnswer'] = False


                    elif '\includegraphics' in data and 'A.' not in data and 'B.' not in data and 'C.' not in data and 'D.' not in data and '(A)' not in data and '(B)' not in data and '(C)' not in data and '(D)' not in data:
                        image = data.replace('\includegraphics', '')
                        image = image.replace('[max width=', '')
                        image = image.replace('textwidth]', '')
                        image = image.replace('\\', '')
                        image = image.replace('}', '')
                        image = image.replace('{', '')
                        image = image.replace('textwidth, center]', '')
                        image = image.replace(' ', '')
                        imgsource = '<img src="https://dieuhanh.vatco.vn//uploads/repository/SUBJECT/' + image + '.png'+ '" >'
                        imgsource = imgsource.replace("textwidth,","")
                        imgsource = imgsource.replace("center]", "")
                        print(imgsource)
                        Lst_ask.append(imgsource)
                    elif data == '':
                        pass
                    else:
                        #Lst_ask.append( '<p>'+  data + '</p>' )
                        Lst_ask.append(data)
                        #print(Lst_ask)
                #print(Lst_ask)
                questassk = '\n'.join(map(str, Lst_ask)).strip().replace('\\\\','')
                #print(questassk)
                Lst_ask.clear()
                dataA = dataA.replace('\\\\','')
                #print(dataA)
                dataB = dataB.replace('\\\\', '')
                #print(dataB)
                dataC = dataC.replace('\\\\', '')
                #print(dataC)
                dataD = dataD.replace('\\\\', '')
                #print(dataD)


                Json_Data['Content'] = str(questassk)
                Json_Data['Solve']['Solver'] = ''
                Json_Data['AnswerData'][0]['Answer'] = str(dataA)
                Json_Data['AnswerData'][1]['Answer'] = str(dataB)
                Json_Data['AnswerData'][2]['Answer'] = str(dataC)
                Json_Data['AnswerData'][3]['Answer'] = str(dataD)
                Json_Data['AnswerData'][0]['ContentDecode'] = str(dataA_decode)
                Json_Data['AnswerData'][1]['ContentDecode'] = str(dataB_decode)
                Json_Data['AnswerData'][2]['ContentDecode'] = str(dataC_decode)
                Json_Data['AnswerData'][3]['ContentDecode'] = str(dataD_decode)

                myUUID = uuid.uuid4()
                str(myUUID)
                Json_Data['Code'] = str(myUUID)
                sleep(0.01)
                myUUID = uuid.uuid4()
                str(myUUID)
                Json_Data['AnswerData'][0]['Code'] = str(myUUID)
                sleep(0.01)
                myUUID = uuid.uuid4()
                str(myUUID)
                Json_Data['AnswerData'][1]['Code'] = str(myUUID)
                sleep(0.01)
                myUUID = uuid.uuid4()
                str(myUUID)
                Json_Data['AnswerData'][2]['Code'] = str(myUUID)
                sleep(0.01)
                myUUID = uuid.uuid4()
                str(myUUID)
                Json_Data['AnswerData'][3]['Code'] = str(myUUID)
                sleep(0.01)
                Json_Data1 = json.dumps(Json_Data)

                Json_Data2 = json.loads(Json_Data1)
                Lst_QUIZZ.append(Json_Data2)
        else:
            fail_file.append(files[0])
            print('check file')


        json_data['SubjectName']= subject_name
        json_data['Title']= Title_name
        json_data['ExamName']= Examname + str(j + 1)

        json_data['Object']['details'] = Lst_QUIZZ
        myUUID = uuid.uuid4()
        json_data['Code'] = str(myUUID)

        #print(json_data)

        data_string = json.dumps(json_data, indent=4)

        pathsave =path_file2
        #(Examname +'-de-so' + str(j + 1)+'.json')
        with open( pathsave + '/' + Examname +'de-so-' + str(j + 1)+'.json', "w") as f:
            f.write(data_string)

print(fail_file)
with open(big_folder + '/'+'LISTFAILE_FAIL.csv', 'w', newline='', encoding="utf-8") as file_output:
    headers = ['PROFILEURL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n', fieldnames=headers)
    writer.writeheader()
    for i in fail_file:
        LinkUrl = i
        writer.writerow({headers[0]: LinkUrl})

