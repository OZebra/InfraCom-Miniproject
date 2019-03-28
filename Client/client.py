##Arquivo para envio

import socket
import os
import argparse
from pathlib import Path

path = os.path.join(os.path.expanduser('~'), 'Desktop', 'miniprojetoinfracom')

serverName = "localhost"
serverPort = 2080

snd = "Send"
upl = "Upload"



try:
    while True:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            clientSocket.connect((serverName,serverPort))
        except Exception:
            pass
        os.system('clear')
        print("Select Database operation: ")
        print("1 - Download from Database")
        print("2 - Upload to Database")
        print("3 - Quit")
        cmd = input("Select option: ")

        if cmd == "1":
            clientSocket.send(snd.encode())

            os.system('clear')
            fileName = input("Enter required file name: ")
            frpath = Path(path + '/Server/Database/' + fileName)
            while not frpath.is_file():
                fileName = input("\nFile not found on server, try another one: ")
                frpath = Path(path + '/Server/Database/' + fileName)

            saveName = input("Enter downloaded file name: ")
            fspath = Path(path + '/Client/' +
Ronaldinho é um cara bem legal!saveName)
            while fspath.is_file():
                saveName = input("\n\nFile already exists, try another name: ")
                fspath = Path(path + '/Client/' + saveName)

            clientSocket.send(fileName.encode())
            fileSize = int(clientSocket.recv(1024).decode())
            print("File size = " + str(fileSize))

            with open(saveName, "xb") as sf:
                data = b''
                while True:
                    print("Receiving file...")
                    aux = clientSocket.recv(1024)
                    if not aux: break
                    data += aux
                    if len(data) >= fileSize: break

                sf.write(data)
                print("File received!\n\n\n")

        elif cmd == "2":
            clientSocket.send(upl.encode())
            os.system('clear')
            ##Envia o nome do arquivo a ser salvo
            fileName = input("Enter the file you want to upload: ")
            fupath = Path(path + '/Client/' + fileName)
            fcpath = Path(path + '/Server/Database/' + fileName)

            while not fupath.is_file():
                fileName = input("\n\nFile do not exists, try another one: ")
                fupath = Path(path + '/Client/' + fileName)

            while fcpath.is_file():
                fileName = input("\nFile already on server, try another one: ")
                fcpath = Path(path + '/Server/Database/' + fileName)

            clientSocket.send(fileName.encode())
            ##Envia o tamanho do arquivo a ser salvo
            with open(fileName, 'rb') as file:
                size = str(len(file.read())*8)
                print("bytesize = " + size)
                clientSocket.send(size.encode())
            ##Envia o arquivo
            with open(fileName, 'r') as file:
                arq = file.read()
                clientSocket.send(arq.encode())



        else:
            break

        clientSocket.close()


        #CMD = 1 == END

except KeyboardInterrupt:
    escape = True
except Exception:
    clientSocket.close()

def getsize(request_string):
    print("entrei")
    with open(request_string, 'rb') as file:
        bytesize = len(file.read())*8
        print("bytesize = " + str(bytesize))
    return str(bytesize)



def send_file(request_string):

    with open(request_string, 'r') as file:
        binData = file.read()

    return binData


clientSocket.close()
print("\nAdios mi amigo!")
