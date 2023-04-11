import glob
import json
import uuid
from time import sleep
import requests
from docx import Document
import os
myUUID = uuid.uuid4()
str(myUUID)
data = {
    "ID": 0,
    "SubjectName": "Toán - 12",
    "Title": "Đề kiểm tra",
    "ExamName": "Đề THPTQG",
    "Error": False,
    "Source": "source_path",
    "Object": {
        "isAlreadyDone": False,
        "details": ""
    },
    "Code": str(myUUID)
}

dict2 = {
    'Id': 'cau',
    'Order': None,
    'Duration': 'Time',
    'Unit': 'MINUTE',
    'Mark': 10,
    'Content': 'title_decode',
    'Solve': {
        'Solver': 'Solve Quest',
        'SolveMedia':[
        {
            'Code': 'VIDEO',
            'Name': 'Video',
            'Icon': 'play',
            'Url': '',
            'Check': False
        },
        {
            'Code': 'IMAGE',
            'Name': 'Image',
            'Icon': 'image',
            'Url': 'title_img',
            'Check': False
        },
        {
            'Code': 'VOICE',
            'Name': 'Voice',
            'Icon': 'microphone-alt',
            'Url': '',
            'Check': False
        }
    ]
    },
    'QuestionMedia': [
        {
            'Code': 'VIDEO',
            'Name': 'Video',
            'Icon': 'play',
            'Url': '',
            'Check': False
        },
        {
            'Code': 'IMAGE',
            'Name': 'Image',
            'Icon': 'image',
            'Url': 'title_img',
            'Check': False
        },
        {
            'Code': 'VOICE',
            'Name': 'Voice',
            'Icon': 'microphone-alt',
            'Url': '',
            'Check': False
        }
    ],
    'Code': 'str(myUUID)',
    'Type': 'QUIZ_SING_CH',
    'AnswerData': 'list_answer',
    'IdQuiz': None,
    'UserChoose': None
}
answerdata = [
{
        'Code': 'str(myUUID)',
        'Answer': 'answer_decode',
        'Url': 'answer_img',
        'Type': "TEXT",
        'ContentDecode': 'answer_get',
        'IsAnswer': None
    },
{
        'Code': 'str(myUUID)',
        'Answer': 'answer_decode',
        'Url': 'answer_img',
        'Type': "TEXT",
        'ContentDecode': 'answer_get',
        'IsAnswer': None
    },
{
        'Code': 'str(myUUID)',
        'Answer': 'answer_decode',
        'Url': 'answer_img',
        'Type': "TEXT",
        'ContentDecode': 'answer_get',
        'IsAnswer': None
    },
{
        'Code': 'str(myUUID)',
        'Answer': 'answer_decode',
        'Url': 'answer_img',
        'Type': "TEXT",
        'ContentDecode': 'answer_get',
        'IsAnswer': None
    }
]

file = r'C:\Users\Server\Downloads\cnv_2022_08_31_0b9960baf410d2d50c1ag\thuvienhoclieucom-de-on-thi-tn-thpt-2022-mon-hoa-phat-trien-tu-de-minh-hoa-de-5--linh-c32dc7b4-be04-40aa-92bc-4e627cb2a31d.docx'


#
data_quest = []
Quest_lst = []
Lst_answer = []
Lst_answerdecode = []
# def get_sourcefile(path):
#     os.chdir(path)
#     for filepath in glob.glob("*.pdf"):
#         filepath =filepath
#     data['Source'] = filepath

def Mathpixconvert():
    options = {
        "conversion_formats": {"docx": True, "tex.zip": True},
        "math_inline_delimiters": ["$", "$"],
        "rm_spaces": True
    }
    r = requests.post("https://api.mathpix.com/v3/pdf",
                      headers={

                          "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac"
                      },
                      data={
                          "options_json": json.dumps(options)
                      },
                      files={
                          "file": open(
                              r"C:\Users\Admin 3i\AppData\Roaming\JetBrains\PyCharmCE2022.1\scratches\doc_lop12_toan_dethi_huy_46c99106.pdf",
                              "rb")
                      }
                      )
    print(r.text.encode("utf8"))
    pdf_id = "2022_06_02_f74debaad6ef9597b517g"
    headers = {
        "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac"
    }

    # get json lines data
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.json"
    response = requests.get(url, headers=headers)
    with open(pdf_id + ".lines.json", "w", encoding='utf-8') as f:
        f.write(response.text)
        print(response.text)
    pass
def TEX2DOCX():
    pass
def checkTF(text):

    if 'TRUE' in text:
        return True
    else:
        return False

def getresult(text):
    if '-A' in text or '-B' in text:
        dapan = text
        dapan = dapan.split('&')
        lst_dapan = []
        for i in dapan:
            if '\\hline' in i and 'A' in i or 'B' in i or 'C' in i or 'D' in i:
                x = i.split('-')
                x[0] = 'Câu' + ' '+str(x[0].replace(' ',''))
                x[0] = str(x[0].replace('\\hline', ''))
                x[1] = str(x[1].replace(' ',''))
                x[1] = str(x[1].replace('\\', ''))
                #print(x)
        #         result['Question'] = x[0]
        #         result['Result'] = x[1]+ '.'
        #         lst_dapan.append(result)
        #
        # Check_result['Check'] = lst_dapan
def getQuestion(text):
    if 'Câu' in text:
        print('paser')
        # need find image
        data_quest.append(text)
        answer_decode = data_quest[0]
        Quest_lst.append(answer_decode)
        data_quest.clear()

        #return answer_decode
    if 'includegraphics' in text:
        text = text.replace('', '')
        Quest_lst.append(text)
        print(text)
        img_name = str(text)
        dict2['QuestionMedia'][1]['Url'] = img_name
    if 'quizz' in text:
        text =text.replace('quizz','')
        data_quest.append(text)
        answer_decode = data_quest[0]
        Quest_lst.append(answer_decode)
        data_quest.clear()
        print(answer_decode)
        pass
    print(len(Quest_lst))
    if len(Quest_lst) == 1:
        answer_decode = ''.join(map(str, Quest_lst))
        Lst_answerdecode.append(answer_decode)
        return Lst_answerdecode
    else:
        answer_decode = ' \n'.join(map(str, Quest_lst))
        Lst_answerdecode.append(answer_decode)
        print(Lst_answerdecode)
        return Lst_answerdecode

def getAnswer(text, ):

    #text_true = result['Result']
    if 'A.' in text:
        A_answer = text
        A_answer = str(A_answer).replace('TRUE','')
        myUUID = uuid.uuid4()
        str(myUUID)
        answerdata[0]['Answer'] = A_answer
        answerdata[0]['Code'] = str(myUUID)
        answerdata[0]['ContentDecode'] = text
        answerdata[0]['IsAnswer'] = checkTF(text)
    if 'B.' in text:
        B_answer = text
        B_answer = str(B_answer).replace('TRUE', '')
        myUUID = uuid.uuid4()
        str(myUUID)
        answerdata[1]['Answer'] = B_answer
        answerdata[1]['Code'] = str(myUUID)
        answerdata[1]['IsAnswer'] = checkTF(text)
        answerdata[1]['ContentDecode'] = text
        Lst_answer.append(answerdata)

    if 'C.' in text:
        C_answer = text
        C_answer = str(C_answer).replace('TRUE', '')
        myUUID = uuid.uuid4()
        str(myUUID)
        answerdata[2]['Answer'] = C_answer
        answerdata[2]['Code'] = str(myUUID)
        answerdata[2]['IsAnswer'] = checkTF(text)
        answerdata[2]['ContentDecode'] = text
        Lst_answer.append(answerdata)
    if 'D.' in text:
        D_answer = text
        D_answer = str(D_answer).replace('TRUE', '')
        myUUID = uuid.uuid4()
        str(myUUID)
        answerdata[3]['Answer'] = D_answer
        answerdata[3]['Code'] = str(myUUID)
        answerdata[3]['IsAnswer'] = checkTF(text)
        answerdata[3]['ContentDecode'] = text
        Lst_answer.append(answerdata)
        return answerdata
def Solve(text):
    lst_solve = []
    if 'Solve' in text:
        text = text.replace('Solve','')
        text = text.replace('Solve_end','')
        lst_solve.append(text)

def Get_Infor(text):
    if 'Môn:' in text:
        subject = text
        subject = ''.join(subject.partition(':')[2:])
        data['SubjectName'] = str(subject)
    if 'ĐÈ KIĖ̀M TRA' in text:
        lecture = text
        data['ExamName'] = str(lecture)
    if 'title' in text:
        title = text
        title = ''.join(title.partition(':')[2:])
        data['Title'] = title
def analyse(directory):
    Lst_finish = []

    doc = Document(directory)
    # if '.docx' in directory:
    for para in doc.paragraphs:
        text = para.text
        #title Note
        Get_Infor(text)
        #getresult(text)
        #text1 = 'Câu 55. AminCH_3 CH_2 NH_2 có tên thay thế là'
        getQuestion(text)
        #return answer_decode
        getAnswer(text)
        #get_sourcefile(path)
        Solve(text)
        #return answerdata
        if 'Solve_end' in text:
            print(Lst_answerdecode)
            dict2['Content'] = Lst_answerdecode[-1]
            dict2['AnswerData'] = answerdata

            dict = json.dumps(dict2)
            Lst_finish.append(dict)
            Lst_answerdecode.clear()
            Quest_lst.clear()
            Lst_answer.clear()
        if 'D.' in text:
            print(Lst_answerdecode)
            dict2['Content'] = Lst_answerdecode[-1]
            dict2['AnswerData'] = answerdata

            dict = json.dumps(dict2)
            Lst_finish.append(dict)
            Lst_answerdecode.clear()
            Quest_lst.clear()
            Lst_answer.clear()

        # if 'D.' in text:
        #     print(Lst_answerdecode)
        #     dict2['Content'] = Lst_answerdecode[-1]
        #     dict2['AnswerData'] = answerdata
        #
        #     dict = json.dumps(dict2)
        #     Lst_finish.append(dict)
        #     Lst_answerdecode.clear()
        #     Quest_lst.clear()
        #     Lst_answer.clear()

    Lst = []
    for i in Lst_finish:
        x = json.loads(i)
        Lst.append(x)
    #print(Lst)
    write2Json(Lst)

def write2Json(Data):
    data['Object']['details'] = Data
    data_string = json.dumps(data, indent=4)

    # file name with extension
    file_name = os.path.basename(file)
    file_name = os.path.splitext(file_name)[0]
    filename = file_name + '.json'
    #print(filename)
    with open(r'F:\PycharmProjects\Source\analyzedata\Json/'+filename, "w") as f:
        f.write(data_string)


analyse(file)