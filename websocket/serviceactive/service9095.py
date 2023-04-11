import websocket.test2.Runsocket
import websocket.test2.sever_boardcast9095

def service_func():
    print('service func')
    websocket.test2.sever_boardcast9095.active9095()
if __name__ == '__main__':
    # service.py executed as script
    # do something
    service_func()