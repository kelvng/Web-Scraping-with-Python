import json
import random
import sys
from datetime import datetime
import time
import pandas as pd
import urllib.request
import requests
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from azcaptchaapi import AZCaptchaApi
from tqdm import tqdm
import websockets
import asyncio
from websocket import create_connection
from pynput import keyboard
# spider_name
name = 'Tailieu'



class websocketclient:

    def __init__(self):
        self.connection = None


    mx = 1
    async def connect(self ):

        self.connection = await websockets.connect('ws://127.0.0.1:6565')
        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            # Send greeting
            while self.mx < 10:
                self.mx += 1
                await self.sendMessage('Hey server, this is webSocket client' + str(self.mx))


            return self.connection




    # async def numbcount(self, numb):
    #     while numb < 10:
    #         numb += 1
    #         sleep(2)
    #         # await self.connection.send(str(numb))
    #         # await self.sendMessage(str(numb))
    #         print(numb)
    #
    #         await self.connection.send(str(numb))

    async def sendMessage(self, message):

        await self.connection.send(str(message))

    async def receiveMessage(self, connection):
        while True:
            try:
                message = await connection.recv()
                print('Received message from server: ' + str(message))
                # if message == 'stop':
                #     sys.exit()
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break
    async def heartbeat(self, connection):
        while True:
            try:
                await connection.send('ping')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break


def numbcount(_num):
    _idx = 0
    while _idx < _num:
        _idx += 1
        sleep(2)
        # await self.connection.send(str(numb))
        # await self.sendMessage(str(numb))
        #await websocketclient.sendMessage(str(_idx))
        print(str(_idx))


if __name__ == '__main__':
    #numbcount(10)
# Creating client object
    client = websocketclient()
    loop = asyncio.get_event_loop()

    # Start connection and get client connection protocol
    connection = loop.run_until_complete(client.connect())

    # Start listener and heartbeat
    tasks = [
        asyncio.ensure_future(client.heartbeat(connection)),
        asyncio.ensure_future(client.receiveMessage(connection)),
    ]

    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_forever()



# async def listen():
#     url = "ws://127.0.0.1:6565"
#     # Connect to the server
#     async with websockets.connect(url) as ws:
#         # greeting message
#         while True:
#             msg = await ws.recv()
#             await ws.send(msg)
#             print(msg)
# asyncio.get_event_loop().run_until_complete(listen())
# asyncio.get_event_loop().run_forever()



