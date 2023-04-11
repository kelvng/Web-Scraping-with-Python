import sys

import websockets
import asyncio
from time import sleep
import json
# url = "ws://127.0.0.1:6565"
# ws = create_connection(url)
# def numbcount(_num):
#     _idx = 0
#     while _idx < _num:
#         _idx += 1
#         sleep(1)
#         ws.send(str(_idx))
#         #print(str(_idx))
# numbcount(10)

async def dem(numb):
    url = "ws://127.0.0.1:9095"
    async with websockets.connect(url) as wb:
        await wb.send('start dem')
    for i in numb:
        url = "ws://127.0.0.1:9095"
        async with websockets.connect(url) as ws:
            print(i)
            await ws.send(i)
            print('------')
            sleep(2)
async def listen():
    url = "ws://127.0.0.1:9095"
    async with websockets.connect(url) as wb:
        while True:
            msg = await wb.recv()
            print(msg)
            if 'num' in msg:
                msg = json.loads(msg)
                print(msg)
                numb = msg['num']
                print(dem)
                asyncio.create_task(dem(numb))
asyncio.get_event_loop().run_until_complete(listen())
asyncio.get_event_loop().run_forever()