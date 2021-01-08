import sys
import os
import binascii
import random

def stringToBinary(str):
    ''' (str) -> str
    >>> stringToBinary("hello world")
    0110100001100101011011000110110001101111001000000111011101101111011100100110110001100100
    >>>stringToBinary("bonjour le monde")
    01100010011011110110111001101010011011110111010101110010001000000110110001100101001000000110110101101111011011100110010001100101
    >>>stringToBinary("hi !!!")
    011010000110100100100000001000010010000100100001
    '''
    return "".join(f"{ord(i):08b}" for i in str)



def binaryToString(string):
    ''' (str) -> str
    >>> binaryToString("0110100001100101011011000110110001101111001000000111011101101111011100100110110001100100")
    hello world
    >>>binaryToString("01100010011011110110111001101010011011110111010101110010001000000110110001100101001000000110110101101111011011100110010001100101")
    bonjour le monde
    >>>binaryToString("01101000 01101001 00100000 00100001 00100001 00100001")
    hi !!!
    '''
    out = [(string[i:i+8]) for i in range(0, len(string), 8)]
    return "".join([chr(int(binary, 2)) for binary in out])


def random384():
    rand = ''
    for i in range(384):
        rand += str(random.randint(0, 1))
    return rand

def random2000Byte():
    rand = ''
    for i in range(16000):
        rand += str(random.randint(0, 1))
    return rand

def generateFiles(path):
    try:
        os.mkdir(path)
    except OSError:
        print ()
    else:
        print ("Successfully created the directory %s " % path)

    folder = path + '/' + '{0:04}'.format(len(os.listdir(path)))
    os.mkdir(folder)

    for x in range(100):
        file = folder + '/' + '{0:02}'.format(x)
        f = open(file + 'c.txt', "w")
        f.write(random2000Byte())
        f.close()
        f = open(file + 'p.txt', "w")
        f.write(random384())
        f.close()
        f = open(file + 's.txt', "w")
        f.write(random384())
        f.close()

def getFiles(path):
    
    folder = path + '/' + os.listdir(path)[0] + '/'
    
    for x in range(100):
        fileC = folder + '{0:02}'.format(x) + 'c.txt'
        fileS = folder + '{0:02}'.format(x) + 's.txt'
        fileP = folder + '{0:02}'.format(x) + 'p.txt'
        fileT = path + '-' + os.listdir(path)[0] + '-' + '{0:02}'.format(x) + 't.txt'
        
        if os.path.isfile(fileC):
            break

        
    return fileC,  fileS, fileP, fileT

    
def xor(message, fileC):
    f = open(fileC, "r")
    c = f.read()
    binaryMesaage = stringToBinary(message)
    y = int(binaryMesaage,2) ^ int(c,2)
    f.close()

    return y

def removeFile(fileC):
    os.remove(fileC)

def addPreSuf(encryptMessage, fileS, fileP):

    f = open(fileS, "r")
    suf = f.read()
    f.close()
    f = open(fileP, "r")
    pre = f.read()
    f.close()
    res = str(suf) + str(encryptMessage)
    res += str(pre)

    return res

def send(message, path):
    
    fileC, fileS, fileP, fileT = getFiles(path)

    encryptMessage = xor(message, fileC)

    encryptMessage = addPreSuf(encryptMessage, fileS, fileP)

    f = open(fileT, "w")
    f.write(encryptMessage)
    f.close()
    removeFile(fileC)


if __name__ != '__main__':
    print("This file was loaded as a module.")
else:
    import argparse as ap

    p = ap.ArgumentParser()
    #p.add_argument("-g", '--generate', action='store_true', help='generate files')
    p.add_argument('folder', help='parent folder')
    p.add_argument("-t", '--text', help='text')
    args = p.parse_args()
    
    folder = ''
    if args.folder:
        folder = args.folder
        generateFiles(args.folder)
    else:
        generateFiles('folder')
    
    if args.text:
        send(args.text, folder)
    else:
        text = input("Enter the text : ") 
        send(text, folder)

