import websocket.test2.Runsocket
import websocket.test2.sever_boardcast9097

def service_func():
    print('service func')
    websocket.test2.sever_boardcast9097.active9097()
if __name__ == '__main__':
    # service.py executed as script
    # do something
    service_func()