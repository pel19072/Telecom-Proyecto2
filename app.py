'''
python -m PyQt5.uic.pyuic -x GUI.ui -o Interfaz.py --> to generate the python
code from the ui created in PyQtDesigner
'''
#************************** GUI Related Imports *******************************#
from Interface import *
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSlot, Qt, QPoint
from PyQt6.QtGui import QFont, QEnterEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt6 import QtCore

#************************* Web Browser Related Imports ************************#
import os
import sys
import time
import socket
import re
import threading

#**************************** Variables Globales ******************************#
url = 'http://zoobank.explorers-log.com/Api?region=es'
domain = ''
url_object = ''
browsing = 0

#************************************* APP ************************************#
class APP (QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__ (self):
        super().__init__()
        self.setupUi(self)
        #******************************* Events *******************************#
        self.pushButton.clicked.connect(self.browse)
        self.pushButton_2.clicked.connect(self.dns_lookup)
        #****************************** Threads *******************************#
        http = threading.Thread(daemon=True,target=http_handler)
        http.start()
        dns = threading.Thread(daemon=True,target=dns_handler)
        dns.start()

    #******************************** Handlers ********************************#
    '''
        Nótese que las siguientes funciones corresponden a un handler de cada
        evento, ya sea de el click de algún botón o del timeout del timer. En
        todos los handlers se utilizan las variables globales para que realmente
        afecten a las mismas variables
    '''
    def browse(self):
        global url, domain, url_object, browsing
        # Filter the URL
        if 'https://' in url:
            url = url.replace('https://', '')
        if 'http://' in url:
            url = url.replace('http://', '')
        domain = re.findall('[0-9a-zA-Z\-\_]*\.[0-9a-zA-Z\-\_]*\.[0-9a-zA-Z\-\_]*', url)
        domain = domain[0]
        url_object = url.replace(domain, '')
        browsing = 1

    def dns_lookup(self):
        pass

#******************************** External Handlers ********************************#
def http_handler():
    global url, domain, url_object, browsing
    while (True):
        if not browsing:
            continue
        # Make the socket connection
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.bind(('', 51472))
        mysocket.connect((domain, 80))

        # Craft the command to be sent with http protocol
        cmd = 'GET {} HTTP/1.1\r\n'.format(url_object)
        cmd += 'Host: {}\r\n'.format(domain)
        cmd += 'Connection: keep-alive\r\n'
        cmd += 'Upgrade-Insecure-Requests: 1\r\n'
        cmd += 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480\r\n'
        cmd += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
        cmd += 'Accept-Encoding: gzip, deflate\r\n'
        cmd += 'Accept-Language: en-US,en;q=0.9\r\n\r\n'
        cmd = cmd.encode()
        mysocket.send(cmd)

        # Receive the get response
        while True:
            data = mysocket.recv(512)
            if not data:
                break
            try:
                print(data.decode())
            except:
                print('cant decode')
        mysocket.close()
        browsing = 0
        

def dns_handler():
    pass

# Inicializa la aplicación y se le da el estilo importado del documento Style.py
app = QtWidgets.QApplication([])
ventanamain=APP()
ventanamain.show()
app.exec()