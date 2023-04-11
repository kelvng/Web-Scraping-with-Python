import requests
import json

options = {
"url": "https://drive.google.com/file/d/1PP62RchcW96k6xOc_KGchsjShKdX4jwE/view?usp=sharing",
    "conversion_formats": {"docx": True, "tex.zip": True},
    "rm_spaces": True
}
r = requests.post("https://api.mathpix.com/v3/pdf",
  headers={

      "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac"
  },
  data={
      "options_json": json.dumps(options)
  }
  )
headers={
      "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac"
  }
print(r.text.encode("utf8"))
my_bytes_value = r.text.encode("utf8")
my_json = my_bytes_value.decode('utf8').replace("'", '"')
#print(my_json)
data = json.loads(my_json)
print("PDF ID: " + data['pdf_id'])
# pdf_id = data['pdf_id']
# path = r'F:\PycharmProjects\Source\analyzedata\filedata'
# # get docx response
# url = "https://api.mathpix.com/v3/pdf/" + '2022_08_29_f508b34ddadc8c2e3617g' + ".docx"
# response = requests.get(url, headers=headers)
# print(response.text)
# with open(pdf_id + ".docx", "wb") as f:
#     f.write(response.content)
# # get LaTeX zip file
# url = "https://api.mathpix.com/v3/pdf/" + '2022_08_29_f508b34ddadc8c2e3617g' + ".tex"
# response = requests.get(url, headers=headers)
# print(response.text)
# with open(pdf_id + ".tex.zip", "wb") as f:
#     f.write(response.content)
