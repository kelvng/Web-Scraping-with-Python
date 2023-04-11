import websocket.test2.Runsocket
import websocket.test2.sever_boardcast9096

def service_func():
    print('service func')
    websocket.test2.sever_boardcast9096.active9096()
if __name__ == '__main__':
    # service.py executed as script
    # do something
    service_func()