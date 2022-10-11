import socket
import re
import sys
import time

def char_hex(numero):
    numero = int(numero)
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



def separar1(url, num):
    partes = url.split(".")
    chars = char_hex(len(partes[0]))
    if num ==1:
        url_final = chars
    else:
        url_final = ""
        chars = chars[2:]
        for i in range(len(chars)):
            coso = chr(int(chars[i], 16))
            url_final += coso
        url_final = str(len(partes[0]))
    for i in range(len(partes)):
        url_final += partes[i]
        if i == len(partes)-1:
            break
        chars = char_hex(len(partes[i+1]))
        if num ==1:
            url_final += chars
        else:
            '''
            chars = chars[2:]
            for i in range(len(chars)):
                coso = chr(int(chars[i], 16))
                url_final += coso
                '''
            url_final += str(len(partes[i+1]))

    return url_final

def dns_answer(data, despues):
    prueba = str(data)
    prueba = prueba.split(despues)
    final = []
    for a in range(len(prueba)-1):
        final = prueba[a+1]
        print(a)
        print(final)
    print("final: "+ str(final)+"\nPrueba: "+str(prueba))
    print("Despues: "+despues)
    
    final = final.replace("\\x", " ")
    lista = final.split(" ")
    try:
        lista.remove("")
    except:
        pass
    final = []
    #print(lista)
    for char in lista:
        if len(char) > 2:
            #print(char[:2])
            final.append(str(char[:2]))
            for i in range(len(char[2:])):
                num = str(hex(ord(char[i+2])))
            #    print(num[2:] +" = "+ char[i+2])
                final.append(str(num[2:]))
        else:
            #print(char[:2])
            final.append(str(char[:2]))
            
    return final[1:]

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
    print(separar(url, 0))
    print(separar(url, 1))
    cmd = cmd1 + url1 + cmd2
    cmd = cmd.encode()
    mysocket.send(cmd)
    
    # RECIBIR QUEARY ANSWER
    data = mysocket.recv(2048)  # Receive the response
    print("\nEnviado ("+cmd1 + url1 + cmd2+")")
    print(data)
    
    answer = dns_answer(data, separar(url, 1))
    #print(formato(dns_answer(data, partes[-1])))
    print(answer)
    print("length: "+str(int("0x"+ answer[14]+answer[15], 16)))
    mysocket.close()


#NSLookup('facebook.com', '8.8.8.8', 'A')
#NSLookup('www.yahoo.com', '8.8.8.8', 'A')
#NSLookup('www.tigo.com.gt', '8.8.8.8', 'A')
NSLookup('uvg.instructure.com', '8.8.8.8', 'A')
#NSLookup('tigo.com.gt', '8.8.8.8', 'A')
