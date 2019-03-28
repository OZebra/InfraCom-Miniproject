#!/usr/bin/env python3
import os
import sys
import itertools
import socket
from socket import socket as Socket


def main():

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(('', 2080))
        server_socket.listen(1)

        print("========================================================")
        print("==================== Zebra Database ====================")
        print("========================================================")
        print("\n\n")
        print("Up and running!")
        print("\n\n")

        contador = 0

        while True:

            with server_socket.accept()[0] as connection_socket:
                operation = connection_socket.recv(1024).decode('ascii')
                print("Selected Operation: " + operation)

                if operation == "Send":

                    request = connection_socket.recv(1024).decode('ascii')

                    size = send_size(request)
                    connection_socket.send(size.encode())

                    arq = send_file(request)
                    print("Sending file...")
                    connection_socket.send(arq.encode())
                    print("File sent!")
                else:
                    ##Recebe o nome do arquivo a ser salvo
                    storeFileName = connection_socket.recv(1024).decode('ascii')
                    print("To-Save file name: " + storeFileName + "\n")
                    ##Recebe o tamanho do arquivo a ser salvo
                    storeFileSize = int(connection_socket.recv(1024).decode())
                    print("To-save file size: " + str(storeFileSize))
                    ##Cria o arquivo que está sendo upado
                    with open('Database/' + storeFileName, "xb") as sf:
                        data = b''
                        while True:
                            print("Receiving file...")
                            aux = connection_socket.recv(1024)
                            if not aux: break
                            data += aux
                            if len(data) >= storeFileSize: break

                        sf.write(data)
                        print("File received!\n\n\n")
            contador += 1
            print("\n\nNumber of requests: " + str(contador) + "\n\n")

    return 0


def send_size(request_string):
    print('Requested file: ' + request_string)

    assert not isinstance(request_string, bytes)

    with open('Database/' + request_string, 'rb') as file:
        bytesize = len(file.read())*8

    print('Required file size: ' + str(bytesize))

    return str(bytesize)



def send_file(request_string):

    with open('Database/' + request_string, 'r') as file:
        binData = file.read()

    return binData



def http_handle(request_string):

    print('Requested file: ' + request_string)

    assert not isinstance(request_string, bytes)

    contents = ''
    with open('Database/' + request_string, 'rb') as file:
        bytesize = len(file.read())*8
        #contents = file.read()
    print('contents: ' + contents)

    return contents

if __name__ == "__main__":
    sys.exit(main())
