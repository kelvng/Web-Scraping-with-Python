# Importing the relevant libraries
from datetime import time

import websockets
import asyncio
import os

# Server data


HOST = "192.168.1.120"
PORT = 9094
print("Server listening on Port " + str(PORT))
# A set of connected ws clients
connected = set()
dotNetClients = set()
scrapyrtClients = set()

# The main behavior function for this server
async def echo(websocket, path):
    print("A client just connected")
    connected.add(websocket)
    try:
        async for message in websocket:
            print("Received message from client: " + message)


            # # Send a response to all connected clients except sender
            print(connected)
            for conn in connected:


                if conn != websocket:
                    await conn.send(message)
                else:
                    if 'Stop Server 9094' in message:
                        print('Stop Server')
                        asyncio.get_event_loop().stop()


    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        connected.remove(websocket)

# Start the server

start_server = websockets.serve(echo, host=HOST, port=PORT, ping_interval=None)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

async def heartbeat():
    '''
    Sending heartbeat to server every 5 seconds
    Ping - pong messages to verify connection is alive
    '''
    try:
        print(connected)
        for conn in connected:
            print("9094 Alive")
            await conn.send('9094 Alive')
        await asyncio.sleep(10)
    except websockets.exceptions.ConnectionClosed:
        print('Connection with server closed')
#
# async def main():
#     task1 = asyncio.create_task(heartbeat())
#     await asyncio.sleep(10)
#     await task1
#
# async def forever():
#     while True:
#         await main()
#
# asyncio.get_event_loop().run_until_complete(forever())
# asyncio.get_event_loop().run_forever()
#
# print('Stop')
# time.sleep(5)

