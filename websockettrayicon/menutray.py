import os
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QMainWindow,QPushButton
from PyQt5.QtCore import Qt,QThread
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import json
import websocket.serviceactive.Stop9094

def click_start():

    print('start button 1')
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Widget.ui', self)
        self.Start  = self.findChild(QPushButton,"StartButton_7")
        self.Stop = self.findChild(QPushButton,'StopButton_9')
        self.Start1 = self.findChild(QPushButton, 'StartButton_10')
        self.Stop1 = self.findChild(QPushButton, 'StopButton_7')
        self.Start.clicked.connect(self.StartSocket9094)
        self.Start1.clicked.connect(self.StartSocket9095)
        self.Stop.clicked.connect(self.StopSocket9094)
        self.Stop1.clicked.connect(self.StopSocket9095)

    def StartSocket9094(self):
        print("Start")
        data = {
            "Port" : "9094",
        }
        url_upload = 'http://localhost:6002/PythonCrawler/ActiveSocket'
        resp = requests.post(url_upload, data=data)
        if resp.ok:
            print(resp.text)
        else:
            print("Something went wrong!")
        self.Start.setEnabled(False)

    def StopSocket9094(self):
        print("Stop")
        data = {
            "Port": "9094",
        }
        url_upload = 'http://localhost:6002/PythonCrawler/StopSocket'
        resp = requests.post(url_upload, data=data)
        if resp.ok:
            print(resp.text)
        else:
            print("Something went wrong!")
        self.Start.setEnabled(True)

    def StartSocket9095(self):
        print("Start")
        data = {
            "Port": "9095",
        }
        url_upload = 'http://localhost:6002/PythonCrawler/ActiveSocket'
        resp = requests.post(url_upload, data=data)
        if resp.ok:
            print(resp.text)
        else:
            print("Something went wrong!")
        self.Start1.setEnabled(False)
    def StopSocket9095(self):
        print("test")
        data = {
            "Port": "9095",
        }
        url_upload = 'http://localhost:6002/PythonCrawler/StopSocket'
        resp = requests.post(url_upload, data=data)
        if resp.ok:
            print(resp.text)
        else:
            print("Something went wrong!")
        self.Start1.setEnabled(True)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing window...')