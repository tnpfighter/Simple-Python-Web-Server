from socket import *
import sys

serverPort = 6789
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('0.0.0.0', serverPort))
serverSocket.listen(1)


while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        requestParts = message.split()
        if len(requestParts) > 1:
            filename = requestParts[1]
            with open(filename[1:]) as f:
                outputdata = f.read()

            header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
            connectionSocket.send(header.encode())
            connectionSocket.send(outputdata.encode())
        else:
            raise IOError
    except IOError:
        header = 'HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n'
        try:
            connectionSocket.send(header.encode())
            error_message = "<html><body>404 Not Found</body></html>"
            connectionSocket.send(error_message.encode())
        except ConnectionAbortedError as e:
            print(f'Error sending data: {e}')
    finally:
        connectionSocket.close()

serverSocket.close()
sys.exit()

