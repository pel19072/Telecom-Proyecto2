import socket
import re
import sys

def NSLookup(url, servidor, tipo):
    # Filter the URL
    if 'https://' in url:
        url = url.replace('https://', '')
    if 'http://' in url:
        url = url.replace('http://', '')
    print(url)
   
    port = 51768
    google_ip = "172.217.15.196"
    
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind(('', port))
    mysocket.connect((servidor, 53))
    print ("se conecto a: "+ servidor)

     # Craft the command to be sent with http protocol
    cmd = ''
    cmd = cmd.encode()
    mysocket.send(cmd)

    # Receive the get response
    '''
    while True:
        data = mysocket.recv(512)
        if not data:
            break
        try:
            print('')
        except:
            print('cant decode')
    mysocket.close()
    '''
    mysocket.close()

NSLookup('tigo.com.gt', '8.8.8.8', 'A')