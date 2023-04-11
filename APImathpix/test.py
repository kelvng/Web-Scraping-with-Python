import requests
import json


import requests

pdf_id = "2022_06_17_5869c8985f99b366bbe5g"
headers = {
  "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac"
}

# get json lines data
url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.json"
response = requests.get(url, headers=headers)
print(response.text)
with open("testtttttt " + ".lines.json", "w") as f:
    f.write(response.text)