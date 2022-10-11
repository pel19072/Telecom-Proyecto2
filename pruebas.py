def toBytes(arr):
    lista = list(arr)
    final = []
    for a in lista:
        print("\n Caracter: "+a)
        print(ord(a))
        final.append(a)
    return final

def char_hex(numero):
    if numero < 16:
        num_hex = hex(numero)
        chars = "\\x0"+num_hex[2:]
        print(chars)
    else:
        num_hex = hex(numero)
        chars = "\\x"+num_hex[2:]
        print(chars)
    return chars

def separar(url, num):
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
    for i in range(len(partes)):
        url_final += partes[i]
        if i == len(partes)-1:
            break
        chars = char_hex(len(partes[i+1]))
        if num ==1:
            url_final += chars
        else:
            chars = chars[2:]
            for i in range(len(chars)):
                coso = chr(int(chars[i], 16))
                url_final += coso
    return url_final

print(separar("uvg.instructure.com", 1))

'''print(type(string[2:]))
chars = string[2:]
for i in range(len(chars)):
    coso = chr(int(chars[i], 16))
    print(coso)'''

'''char2 = '2b'
char1 = '4c'
char2 = "0x"+char2
char1 = "0x"+char1
num1 = int(char1, 16)
num2 = int(char2, 16)
num = num2*16**2 + num1
print(num)'''

'''
def separar(url):
    partes = url.split(".")

    url = chr(len(partes[0]))
    for i in range(len(partes)):
        url += partes[i]
        if i == len(partes)-1:
            break
        url += chr(len(partes[i]))
    return url

print(separar("www.tigo.com.gt"))
prueba = b'\x03'
print(prueba.decode("ascii"))
'''

'''
num = {}
num["yahoo.com"] = "05 79 61 68 6f 6f 03 63 6f 6d 00 00 00 00 00 00"
num["www.yahoo.com"] = "03 77 77 77 05 79 61 68 6f 6f 03 63 6f 6d 00 00 01 00 01"
num["tigo.com.gt"] = "04 74 69 67 6f 03 63 6f 6d 02 67 74 00 00 01 00 01"

for dominio in num:
    num[dominio] = num[dominio].split(" ")
    string = ""
    for char in num[dominio]:
        char = "0x"+char
        entero = int(char, 16)
        string += chr(entero)
    print(string)
'''

'''
        ID          = 02        2 bytes

        QR          = 0         1 bit       1
        Opcode      = 0000      4 bits      5
        bit en medio de AA (answer)         6
        Truncated   = 0         1 bit       7
        Recursion   = 1         1 bit       1 byte

        Recursion available (answer)        1
        Z           = 000       3 bits      4
        RCode       = 0000      4 bits      1 byte

        QDCount     = 01        2 bytes

        ANCount     (answer)    2 bytes 

        NSCount     (answer)    2 bytes  

        ARCount     (answer)    2 bytes

    '''