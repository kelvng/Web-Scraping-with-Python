from docx2pdf import convert
import requests
import json
import aspose.words as aw
import os
import shutil, os
def docx_pdf (file_docx,local_pdf):
    #convert("input.docx")
    # file_docx = r"F:\PycharmProjects\Source\analyzedata\converttest\docx\thuvienhoclieu.com-De-on-thi-TN-THPT-2022-mon-Hoa-phat-trien-tu-de-minh-hoa-De-4.docx"
    # local_pdf = r"F:\PycharmProjects\Source\analyzedata\converttest\PDF\thuvienhoclieu.com-De-on-thi-TN-THPT-2022-mon-Hoa-phat-trien-tu-de-minh-hoa-De-4.pdf"
    convert(file_docx, local_pdf)
    #convert("my_docx_folder/")
def doc_pdf(file_doc,local_pdf):
    # Load word document
    #file_doc = r"F:\PycharmProjects\Source\analyzedata\converttest\doc\doc_lop1_ATGT_baigiang_linh_d7435909.doc"
    doc = aw.Document(file_doc)
    #local_pdf = r"F:\PycharmProjects\Source\analyzedata\converttest\PDF\doc_lop1_ATGT_baigiang_linh_d7435909.pdf"
    # Save as PDF
    doc.save(local_pdf)

folder_in = input("path file of in folder: ")
input1 = folder_in
dir_path = input1

folder_out = input("path file of in folder: ")
output1 = folder_out
# folder path

# list file and directories
res = os.listdir(dir_path)
print(res)
dem = 0
lst_error = []
check_mode = input("entercheckmode : 'CONVERT' or 'COPY' :")
if check_mode == 'CONVERT':
    try:
        for filename in res:

            inputpath = dir_path + '\\' + filename
            print(inputpath)
            if '.docx' in filename:
                output = output1 + '\\' + filename.replace('.docx','.pdf')
                docx_pdf(inputpath,output)
                pass
            elif '.doc' in filename:
                output = output1 + '\\' + filename.replace('.doc', '.pdf')
                doc_pdf(inputpath,output)
                pass
            elif '.pdf' in filename:
                #output = output + '\\' + filename.replace('.doc', '.pdf')

                pass
            else:
                dem = dem +1
                lst_error.append(filename)
                print(filename)
    except:
        pass
elif check_mode == 'COPY':
    try:
        for filename in res:

            inputpath = dir_path + '\\' + filename
            print(inputpath)
            if '.docx' in filename:
                shutil.move(inputpath,output1 + '\\' + filename)
                pass
            elif '.doc' in filename:
                shutil.move(inputpath, output1 + '\\' + filename)
                pass
            elif '.pdf' in filename:
                #shutil.copy(inputpath, output1 + '\\' + filename)
                pass
            else:
                dem = dem + 1
                lst_error.append(filename)
                print(filename)
    except:
        pass

print(dem)
print(lst_error)





#docx_pdf(r'P:\datacrawl\Thuvienhoclieu.com\Đề Thi Thử Tốt Nghiệp THPT Môn Sinh 2022\thuvienhoclieu.com-De-thi-thu-TN-THPT-2022-Sinh-Truong-Tran-Quoc-Tuan-lan-1-co-dap-an.docx',r'P:\datacrawl\Thuvienhoclieu.com\Đề Thi Thử Tốt Nghiệp THPT Môn Sinh 2022\thuvienhoclieu.com-De-thi-thu-TN-THPT-2022-Sinh-Truong-Tran-Quoc-Tuan-lan-1-co-dap-an.pdf')




# with open(r'C:\Users\Server\AppData\Roaming\JetBrains\PyCharmCE2020.2\scratches\data.json', 'r') as f:
#     json_string = json.load(f)
# print(json_string)
# Folder_ID = input('enter ur folder ID: ')
# json_string['ParentId'] = Folder_ID
# print(json_string)
# url_upload = 'http://localhost:6002/PythonCrawler/JtableFileWithRepository'
#
#
# #response = requests.request("POST", url_upload,json = param )
# response = requests.request("POST", url_upload, json = json_string)
# print(response)
# data = response.text
# dataJson = json.loads(data)
# print(dataJson)
# list_file = dataJson['data']
# print(list_file)
# for i in range(len(list_file)):
#     File_Id = list_file[i]['Id']
#     Is_File = list_file[i]['IsDirectory']
#     File_Name = list_file[i]['FileName']
#     File_Type = list_file[i]['MimeType']
#     print(File_Id)
#     print(Is_File)
#     print(File_Name)
#     print(File_Type)
#     print('--------------------------')
#     if Is_File ==True:
#         if File_Type  == 'application/msword':
#             print('doc')
#
#             pass
#         elif File_Type  == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
#             pass
#             print('docx')
#         else:
#             pass
#     else:
#         fodler_Id = Is_File