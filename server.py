import socket
import os

# create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a specific address and port
server_address = ('localhost', 8080)
server_socket.bind(server_address)

# listen for incoming connections
server_socket.listen(1)

print(f"Server is on {server_address}")

while True:
    # wait for a client connection
    client_socket, client_address = server_socket.accept()
    
    # receive the HTTP request
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request from {client_address}:")
    print(request)
    
    # parse the request to get the requested file path
    file_path = request.split()[1]
    print(f"Requested file path: {file_path}")
    
    # get the absolute path of the requested file
    absolute_path = os.path.abspath(file_path.strip('/'))

    # check if the file exists
    if not os.path.exists(absolute_path):
        # if the file does not exist, send a 404 Not Found response
        response_status = "HTTP/1.1 404 Not Found\r\n"
        response_body = "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>"
    else:
        # if the file exists, read its contents
        with open(absolute_path, 'r') as f:
            file_contents = f.read()
        
        # create the HTTP response message
        response_status = "HTTP/1.1 200 OK\r\n"
        response_headers = f"Content-Type: text/html\r\nContent-Length: {len(file_contents)}\r\n"
        response_body = file_contents
    
    # combine the response components into a single message
    response_message = response_status + response_headers + "\r\n" + response_body
    
    # send the response to the client
    client_socket.sendall(response_message.encode('utf-8'))

    # close the client connection
    client_socket.close()