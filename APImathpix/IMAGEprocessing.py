import requests
import json

from docx import Document
from PIL import Image
import os

filepath = r"C:\Users\Admin 3i\PycharmProjects\Source\APImathpix\test"
files = os.listdir(filepath)
#list off multifodler
for x in files:
    path = filepath + '\\' + x
    files = os.listdir(path)
    print('-------------')
    Lst_img = []
    for file in files:
        # make sure file is an image
        print(file)
        if file.endswith('.png'):
            Path_remove = path + '\\'
            img_path = Path_remove + file
            Lst_img.append(img_path)
        print(Lst_img)
        mathpix_dataLst = []
        Lst_path = []
        Lst_name = []
        for image_path in Lst_img:
            pathdoc_save = os.path.dirname(image_path)
            Lst_path.append(pathdoc_save)
            name = pathdoc_save.replace(filepath,'')
            name = name.replace('\\','')
            print(name)
            r = requests.post("https://api.mathpix.com/v3/text",
                files={"file": open(image_path,"rb")},
                data={
                  "options_json": json.dumps({
                    "math_inline_delimiters": ["$", "$"],
                    "rm_spaces": True
                  })
                },
                headers={
                    "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac"
                }
            )
            json_data = json.dumps(r.json(), indent=4, sort_keys=True)
            json_data = json.loads(json_data)
            math_text = json_data["text"]
            math_text=math_text.replace('$', '')
            print(math_text)
            mathpix_dataLst.append(math_text)
            namedocx = name + '.docx'
            Lst_name.append(namedocx)
        print(mathpix_dataLst)
        document = Document()
        for value in mathpix_dataLst:

            document.add_paragraph(value)
            document.save(Lst_path[0]+'/'+ Lst_name[0])
        Lst_img.clear()
        mathpix_dataLst.clear()
