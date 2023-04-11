from time import sleep
import sys
import websockets
import asyncio
from websocket import create_connection
import json
import requests
#sipder name
name = ''
flagstop = False
param = ""
async def initspider():
    ws = websockets.connect('ws://127.0.0.1:9091', ping_interval=None)
    async with ws as wb:
        while True:
            param = await wb.recv()
            if param != "":
                break
        data = json.loads(param)
        param1 = data['Url']
        print(param1)
        name = param1
        #runspider(param[0], param[1], param[2])
async def main():

    task_1 = asyncio.create_task(initspider())
    await task_1
if __name__ == '__main__':
    asyncio.run(main())
#runspider with param

# async def runspider(param1, numb):
#     req = requests.get(param1)
#
#     ws = websockets.connect('ws://127.0.0.1:9091', ping_interval=None)
#     async with ws as wb:
#         await ws.send(req)


