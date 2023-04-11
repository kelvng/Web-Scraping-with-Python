# coding=utf8
# -*- coding: utf-8 -*-
from docx import Document
import os

path = r'C:\Users\Admin 3i\PycharmProjects\Source\analyzedata\Data_save\2022_06_02_f74debaad6ef9597b517g\2022_06_02_f74debaad6ef9597b517g.tex'

# file name with extension
file_name = os.path.basename(path)
file_name = os.path.splitext(file_name)[0]
file_name = file_name.replace('.tex', '')

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()
x = text.split('\n')
print(x)
document = Document()

for value in x:
    document.add_paragraph(value)
document.save(file_name + '.docx')

import requests
import json
head = {
        "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac"
    }
# options = {
#     "conversion_formats": {"docx": True, "tex.zip": True},
#     "math_inline_delimiters": ["$", "$"],
#     "rm_spaces": True
# }
# r = requests.post("https://api.mathpix.com/v3/pdf",
#     headers= head,
#     data={
#         "options_json": json.dumps(options)
#     },
#     files={
#         "file": open(r"C:\Users\Admin 3i\Desktop\Download\Download\Lớp_11\đề thi\Vật lý\doc_lop11_vatly_dethi_truong_4a8fb4b3.pdf","rb")
#     }
# )
# x = r.text.encode("utf8")
# y = json.loads(x)
# print(y)
# print(y['pdf_id'])
pdf_id = '2022_06_07_76b7b53d3079eb2e4e75g'
# url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".mmd"
# response = requests.get(url, headers=head)
# with open(pdf_id + ".mmd", "w") as f:
#     f.write(response.text)
# get LaTeX zip file
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".tex"
response = requests.get(url, headers=head)
with open(pdf_id + ".tex.zip", "wb") as f:
    f.write(response.content)
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".docx"
response = requests.get(url, headers=head)
with open(pdf_id + ".docx", "wb") as f:
    f.write(response.content)