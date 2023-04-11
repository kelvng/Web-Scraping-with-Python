from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
# Go to https://my.telegram.org/apps, sign in, go to API development tools, create an app, copy and paste below:
api_id = 0
api_hash = '0'
phone = '+84974384516'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: ')) # Enter the login code sent to your telegram

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
"""
Megagroups are groups of more than 200 people, if you want to leave 
smaller groups as well delete this part. If you want to stay in a few 
specific groups, add their titles to the groups_to_exclude list.
"""
groups_to_exclude = ['group title']

for chat in chats:
    try:
        if chat.megagroup == True and chat.title not in groups_to_exclude:
            client.delete_dialog(chat)
            print(0)
    except:
        continue