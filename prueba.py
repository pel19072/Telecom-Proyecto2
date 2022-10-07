import socket
import re

def browser(url):
    # Filter the URL
    if 'https://' in url:
        url = url.replace('https://', '')
    if 'http://' in url:
        url = url.replace('http://', '')
    domain = re.findall('[0-9a-zA-Z\-\_]*\.[0-9a-zA-Z\-\_]*\.[0-9a-zA-Z\-\_]*', url)
    domain = domain[0]
    url_object = url.replace(domain, '')
    
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
    
browser('http://zoobank.explorers-log.com/Api?region=es')