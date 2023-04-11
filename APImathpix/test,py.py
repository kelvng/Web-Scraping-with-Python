# import requests
# import json
#
# r = requests.post("https://api.mathpix.com/v3/text",
#         json={
#             "src": r"D:\",
#             "math_inline_delimiters": ["$", "$"],
#             "rm_spaces": True
#         },
#         headers={
#             "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac",
#             "Content-type": "application/json"
#         }
#     )
# print(json.dumps(r.json(), indent=4, sort_keys=True))

import requests
import json

# r = requests.post("https://api.mathpix.com/v3/text",
#     files={"file": open(r"C:\Users\Admin 3i\PycharmProjects\Source\APImathpix\Screenshot_1.png","rb")},
#     data={
#       "options_json": json.dumps({
#         "math_inline_delimiters": ["$", "$"],
#         "rm_spaces": True
#       })
#     },
#     headers={
#         "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac"
#     }
# )
# x = json.dumps(r.json(), indent=4, sort_keys=True)
# with open("test.json", 'w') as f:
#     f.write(x)
# import requests
# import json
#
# # put input strokes here
# strokes_string = '{"strokes": {\
#     "x": [[131,131,130,130,131,133,136,146,151,158,161,162,162,162,162,159,155,147,142,137,136,138,143,160,171,190,197,202,202,202,201,194,189,177,170,158,153,150,148],[231,231,233,235,239,248,252,260,264,273,277,280,282,283],[273,272,271,270,267,262,257,249,243,240,237,235,234,234,233,233],[296,296,297,299,300,301,301,302,303,304,305,306,306,305,304,298,294,286,283,281,281,282,284,284,285,287,290,293,294,299,301,308,309,314,315,316]],\
#     "y": [[213,213,212,211,210,208,207,206,206,209,212,217,220,227,230,234,236,238,239,239,239,239,239,239,241,247,252,259,261,264,266,269,270,271,271,271,270,269,268],[231,231,232,235,238,246,249,257,261,267,270,272,273,274],[230,230,230,231,234,240,246,258,268,273,277,281,281,283,283,284],[192,192,191,189,188,187,187,187,188,188,190,193,195,198,200,205,208,213,215,215,215,214,214,214,214,216,218,220,221,223,223,223,223,221,221,220]]\
#   }}'
# strokes = json.loads(strokes_string)
# r = requests.post("https://api.mathpix.com/v3/strokes",
#     json={"strokes": strokes},
#     headers={ "app_key": "b4175fda933a37d03e14640bb900b5103ad65bae91bb33eb88f81c42c8f045ac",
#              "Content-type": "application/json"})
# print(json.dumps(r.json(), indent=4, sort_keys=True))


# import requests
#
#
#
# pdf_id = "PDF_ID"
# headers = {
#   "app_key": "2022_06_17_169924da83759f323d4cg"
# }
#
# # get json lines data
# url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".lines.mmd.json"
# response = requests.get(url, headers=headers)
# with open("hahahahhoho" + ".lines.mmd.json", "w") as f:
#     f.write(response.text)

