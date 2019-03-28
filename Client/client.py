import socket
from os import system
import argparse

serverName = "localhost"
serverPort = 2080

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

parser = argparse.ArgumentParser()
parser.add_argument('--message', '-d', type=str,
                    help='Message to send')
args = parser.parse_args()

print (args.message)

try:
    clientSocket.connect((serverName,serverPort))
except Exception:
    pass

try:
    print("Select Database operation: ")
    print("1 - Download from Database")
    print("2 - Upload to Database")
    cmd = input("Select option: ")

    if cmd == "1":
        system('clear')
        fileName = input("Enter required file name: ")
        saveName = input("Enter downloaded file name: ")

        clientSocket.send(fileName.encode())

        fileSize = int(clientSocket.recv(1024).decode())
        print("Tamanho recebido = " + str(fileSize))

        with open(saveName, "xb") as sf:
            data = b''
            while True:
                print("Receiving file...")
                aux = clientSocket.recv(1024)
                if not aux: break
                data += aux
                if len(data) >= fileSize: break

            sf.write(data)
            print("File received!")

    else:
        system('clear')
        fileName = input("Enter the file you want to upload: ")
    clientSocket.close()


        #CMD = 1 == END

except KeyboardInterrupt:
    escape = True
except Exception:
    clientSocket.close()


clientSocket.close()
print("\nBye bye :)")
