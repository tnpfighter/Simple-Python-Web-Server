# Simple Python Web Server

This project is a simple Python web server capable of processing a single request. It demonstrates the basic principles of socket programming and HTTP request handling.

**March, 2023**

## Overview

The web server performs the following tasks:
1. Creates a connection socket when contacted by a client (browser).
2. Receives the HTTP request from this connection.
3. Parses the request to determine the specific file being requested.
4. Retrieves the requested file from the server’s file system.
5. Creates an HTTP response message consisting of the requested file preceded by header lines.
6. Sends the response over the TCP connection to the requesting browser.
7. If a browser requests a file that is not present in the server, the server returns a “404 Not Found” error message.

## Requirements

- Python 3.x
- Basic knowledge of Python and socket programming

## Files

- `webserver.py`: The main server script.
- `simpleWeb.html`: Example HTML file to be served by the server.

## Setup

1. Place the `webserver.py` and `simpleWeb.html` files in the same directory.
2. Open a terminal and navigate to the directory containing these files.

## Running the Server

1. Run the server script:
   ```sh
   python3 webserver.py
   ```
2. Determine the IP address of the host running the server (e.g., `192.168.0.20`).
3. From another device within the same network, open a web browser and enter the URL:
   ```sh
   http://192.168.0.20:6789/simpleWeb.html
   ```
   Replace `192.168.0.20` with the actual IP address and `6789` with the port number used in the server script.

## Accessing the Server

To test the server:
1. Access an existing file: 
   - The contents of `simpleWeb.html` should be displayed in the browser.
2. Access a non-existing file:
   - The server should return a “404 Not Found” error message.


## Code

The main server code (`webserver.py`) is as follows:

```python
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
```
