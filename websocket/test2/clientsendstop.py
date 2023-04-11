# -*- coding: utf-8 -*-
import struct
import sys

import websockets
import asyncio
import struct

async def listen():
    url = "ws://127.0.0.1:9095"

    # Connect to the server
    async with websockets.connect(url, ) as ws:
        await ws.send('1+1 = ?')




asyncio.get_event_loop().run_until_complete(listen())
