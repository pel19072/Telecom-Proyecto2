from distutils.fancy_getopt import FancyGetopt
import socket
import re
import sys
import time

def char_hex(numero):
    if numero < 16:
        num_hex = hex(numero)
        chars = "\\x0"+num_hex[2:]
    else:
        num_hex = hex(numero)
        chars = "\\x"+num_hex[2:]
    return chars

def separar(url, num):
    partes = url.split(".")
    chars = char_hex(len(partes[0]))
    if num == 1:
        url_final = chars
    else:
        url_final = chr(len(partes[0]))
    for i in range(len(partes)):
        url_final += partes[i]
        if i == len(partes)-1:
            break
        if num == 1:
            url_final += char_hex(len(partes[i+1]))
        else:
            url_final += chr(len(partes[i+1]))
    return url_final

def AnsToData(answer, ind, url):
    length = int(answer[10+ind]+answer[11+ind])
    dominio = int(answer[0])*16**2 + int(answer[1])
    #print("dominio: "+str(dominio))
    temp = []
    data = ''
    tipo = int(answer[ind+2])*10 + int(answer[ind+3])
    #print("Tipo: "+str(tipo)+"\t length: "+str(length))
    numero = True
    i = 0
    coso = False
    for ans in answer[ind+12:ind+12+length]:
        temp_dom = int(answer[i])*16**2 + int(answer[1+i])
        #print(temp_dom)
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
                #print("j = "+ str(j))
                #print(j)
                if j == 192:
                    coso = True
                numero = False
                continue
            if coso:
                if int(ans) == 16 or int(ans)==12:
                    #print("mismo link")
                    data += url
                    continue
            data += chr(int(str(ans)))
            temp.append(chr(int(ans)))
            j -= 1
            if j == 0:
                data += "."
                numero = True
    ind += 12+length
    #print("Length: "+str(length))
    #print("\n"+str(ind)+" de "+ str(len(answer)))
    return [data, ind]


def dns_answer(data):
    final = []
    i = 12
    while True:
        valor = int(data[i])
        i += valor + 1
        if valor == 0:
            break
    final = data[i+4:]
    return final

def NSLookup(url, servidor, tipo):
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
           
    match tipo:
        case 'A':   #  ??  tipo    class
            cmd2 = b'\x00\x00\x01\x00\x01'
        case 'NS':
            cmd2 = b'\x00\x00\x02\x00\x01'
        case 'CNAME':
            cmd2 = b'\x00\x00\x05\x00\x01'
        case _:
            print("El tipo de registro ingresado no es valido")
            return

    cmd2 = cmd2.decode("ascii")
    partes = url.split(".")

    url1 = separar(url, 0)
    cmd = cmd1 + url1 + cmd2
    cmd = cmd.encode()
    mysocket.send(cmd)
    
    # RECIBIR QUEARY ANSWER
    data = mysocket.recv(2048)  # Receive the response
    answer = []
    for a in data:
        answer.append(str(a))
        
    print("\nEnviado ("+cmd1 + url1 + cmd2+")")
    
    #print(formato(dns_answer(data, partes[-1])))
    #print(answer)
    lista = []
    for ans in answer:
        lista.append(chr(int(ans)))
    ind = 0
    answer = dns_answer(answer)
    if partes[0]=="www":
        url = ""
        for i in partes[1:]:
            url += str(i)
            if i != partes[-1]:
                url += "."
        #print(url)
    while ind+10 < len(answer):
        result = AnsToData(answer, ind, url)
        ind = result[1]
        print(str(result[0])) #+"\t\t indice="+str(ind)
    
    mysocket.close()


NSLookup('facebook.com', '8.8.8.8', 'A')
NSLookup('www.yahoo.com', '8.8.8.8', 'NS')
NSLookup('www.tigo.com.gt', '8.8.8.8', 'A')
NSLookup('uvg.instructure.com', '8.8.8.8', 'CNAME')
NSLookup('tigo.com.gt', '8.8.8.8', 'A')
NSLookup('tigo.com.gt', '8.8.8.8', 'NS')
url = 'http://llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch.co.uk'
NSLookup(url, '8.8.8.8', 'A')
NSLookup(url, '8.8.8.8', 'NS')