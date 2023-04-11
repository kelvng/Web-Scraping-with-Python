# importing all required libraries
#import telebot
import requests
import telegram
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import time, telebot

# get your api_id, api_hash, token
# from telegram as described above
api_id = '9759461'
api_hash = 'b5544e9191e6b7742520777b32ce29fd'
token = '5238223755:AAEnpZxoip2NjEr9y-g89zPH74t_ra6O4Y4'
bot = telebot.TeleBot(token)
group = "-640765989"
message = "Working..."

# your phone number
phone = '+84974384516'

# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)

# connecting and building the session
client.connect()
print(1)
# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():
    client.send_code_request(phone)

    # signing in the client
    client.sign_in(phone, input('Enter the code: '))
    print(2)
else:
    print(3)
def sen_message(token):
    Chat=["Hi, I'm bot",
      "Hi, I'm bot",
      "Hi, I'm bot",
      "Hi, I'm bot",
      "Hi, I'm bot",]
    for ms in Chat:
        base_url = 'https://api.telegram.org/bot'+token+'/sendMessage?chat_id='+group+'=&text="{}"'.format(ms)
        requests.get(base_url)
print(2)
sen_message(token)
client.disconnect()
