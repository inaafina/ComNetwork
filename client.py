from socket import *

serverName = input('IP Address : ')
serverPort = int(input('Port : '))

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

filename = input('The file you want to retrieve: ')

request = f"GET /{filename} HTTP/1.1\r\nHost: {serverName}\r\n\r\n"
clientSocket.send(request.encode())

response = clientSocket.recv(1024)

print(response.decodce()) # Print the HTTP response message

if response.decode().startswith('HTTP/1.1 200 OK'): # Save the content of the requested file to a local file
    with open(filename, 'wb') as f:
        while True:
            data = clientSocket.recv(4096)
            if not data:
                break
            f.write(data)
    print('File saved to ',filename)

clientSocket.close()