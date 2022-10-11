'''
python -m PyQt6.uic.pyuic -x Interface.ui -o Interface.py --> to generate the python
code from the ui created in PyQtDesigner
'''
#************************** GUI Related Imports *******************************#
from Interface import *
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QObject, QRunnable, pyqtSlot, QThreadPool, QTimer
from PyQt6.QtGui import QFont, QEnterEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog

#************************* Web Browser Related Imports ************************#
import socket
import re
import threading

#**************************** Variables Globales ******************************#
# HTTP
urls = ['http://www.testingmcafeesites.com/testcat_al.html',
        'http://www.testingmcafeesites.com/testcat_an.html',
        'http://www.testingmcafeesites.com/testcat_au.html',
        'http://www.testingmcafeesites.com/testcat_be.html']
url = urls[0]
domain = ''
url_object = ''
browsing = 0
final_page = ''
# DNS
dns_type = ''
dns_domain = ''
dns_server = ''

#************************************* APP ************************************#
class APP (QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__ (self):
        super().__init__()
        self.setupUi(self)
        #******************************* Events *******************************#
        self.pushButton.clicked.connect(self.browse)
        self.pushButton_2.clicked.connect(self.dns_lookup)
    #******************************** Handlers ********************************#
    '''
        Nótese que las siguientes funciones corresponden a un handler de cada
        evento. En todos los handlers se utilizan las variables globales para 
        que realmente afecten a las mismas variables
    '''
    #********************************** HTTP **********************************#
    def browse(self):
        global url, urls, domain, url_object, browsing, final_page
        if self.lineEdit.text() == '':
            url = urls[0]
        else:         
            url = self.lineEdit.text()
        # Filter the URL
        if 'https://' in url:
            url = url.replace('https://', '')
        if 'http://' in url:
            url = url.replace('http://', '')
        domain = re.findall('.*?/', url) 
        domain = domain[0][:-1]
        print(domain)
        url_object = url.replace(domain, '')
        #browsing = 1
        # Make the socket connection
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            data = mysocket.recv(4096)
            if not data:
                break
            try:
                final_page = final_page + data.decode()
                if '</html>' in data.decode().lower():
                    break
            except Exception as e:
                print(e)
                break         
        mysocket.close()        
        final_page = '<' + final_page.split('<', 1)[1]     
        print(final_page)
        self.textEdit.setHtml(final_page)
        final_page = ''

    #*********************************** DNS **********************************#
    def char_hex(self, numero):
        if numero < 16:
            num_hex = hex(numero)
            chars = "\\x0"+num_hex[2:]
        else:
            num_hex = hex(numero)
            chars = "\\x"+num_hex[2:]
        return chars

    def separar(self, url, num):
        partes = url.split(".")
        chars = self.char_hex(len(partes[0]))
        if num == 1:
            url_final = chars
        else:
            url_final = chr(len(partes[0]))
        for i in range(len(partes)):
            url_final += partes[i]
            if i == len(partes)-1:
                break
            if num == 1:
                url_final += self.char_hex(len(partes[i+1]))
            else:
                url_final += chr(len(partes[i+1]))
        return url_final

    def AnsToData(self, answer, ind, url):
        length = int(answer[10+ind]+answer[11+ind])
        dominio = int(answer[0])*16**2 + int(answer[1])
        temp = []
        data = ''
        tipo = int(answer[ind+2])*10 + int(answer[ind+3])
        numero = True
        i = 0
        coso = False
        for ans in answer[ind+12:ind+12+length]:
            temp_dom = int(answer[i])*16**2 + int(answer[1+i])
            i += 1            
            if tipo == 1:
                temp.append(int(str(ans)))
                if i == length:
                    data += str(int(str(ans)))
                    break
                data += str(int(str(ans)))+ "."
            else:
                if numero:
                    j = int(ans)
                    if j == 192:
                        coso = True
                    numero = False
                    continue
                if coso:
                    if int(ans) == 16 or int(ans)==12:
                        data += url
                        continue
                data += chr(int(str(ans)))
                temp.append(chr(int(ans)))
                j -= 1
                if j == 0:
                    data += "."
                    numero = True
        ind += 12+length
        return [data, ind]

    def dns_answer(self, data):
        final = []
        i = 12
        while True:
            valor = int(data[i])
            i += valor + 1
            if valor == 0:
                break
        final = data[i+4:]
        return final

    def NSLookup(self, url, servidor, tipo):
        # Filter the URL
        if 'https://' in url:
            url = url.replace('https://', '')
        if 'http://' in url:
            url = url.replace('http://', '')
    
        port = 51768
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mysocket.bind(('', port))
        mysocket.connect((servidor, 53))

        # Craft the command to be sent
        cmd1 = b'\x00\x02\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        cmd1 = cmd1.decode("ascii")
            
        if tipo == 'A':   #  ??  tipo    class
            cmd2 = b'\x00\x00\x01\x00\x01'
        elif tipo == 'NS':
            cmd2 = b'\x00\x00\x02\x00\x01'
        elif tipo == 'CNAME':
            cmd2 = b'\x00\x00\x05\x00\x01'
        else:
            print("El tipo de registro ingresado no es valido")
            return

        cmd2 = cmd2.decode("ascii")
        partes = url.split(".")

        url1 = self.separar(url, 0)
        cmd = cmd1 + url1 + cmd2
        cmd = cmd.encode()
        mysocket.send(cmd)
        
        # RECIBIR QUEARY ANSWER
        data = mysocket.recv(2048)  # Receive the response
        answer = []
        for a in data:
            answer.append(str(a))
            
        print("\nEnviado ("+cmd1 + url1 + cmd2+")")
        lista = []
        for ans in answer:
            lista.append(chr(int(ans)))
        ind = 0
        answer = self.dns_answer(answer)
        if partes[0]=="www":
            url = ""
            for i in partes[1:]:
                url += str(i)
                if i != partes[-1]:
                    url += "."
        while ind+10 < len(answer):
            result = self.AnsToData(answer, ind, url)
            ind = result[1]
            print(str(result[0]))        
        mysocket.close()
        self.textEdit_2.setHtml(str(result[0]))
    
    def dns_lookup(self):
        global dns_domain, dns_server, dns_type
        dns_domain = self.lineEdit_2.text()
        dns_server = self.lineEdit_3.text()
        dns_type = self.comboBox.currentText()
        self.NSLookup(dns_domain, dns_server, dns_type)

# Inicializa la aplicación
app = QtWidgets.QApplication([])
ventanamain=APP()
ventanamain.show()
app.exec()