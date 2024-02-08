from socket import *

#Create a TCP server socket
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)

while True:
    #Establish the connection
    print("The server is ready to receive")
    connectionSocket, addr = serverSocket.accept() #modified here
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open("./html_files/" + filename[1:])
        outputdata = f.read()

        #Send HTTP OK and the Set-Cookie header into the socket
        # set the cookie to whatever value you'd like
        httpOK = 'HTTP/1.0 200 OK\r\nSet-Cookie: cookie1=987654321\r\nContent-Type: text/html\r\n\n<h1>boy oh boy do i love computer networking</h1>\r\n'
        connectionSocket.send(httpOK.encode())

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        # Close the socket
        connectionSocket.close()
    except IOError:
        #Send HTTP NotFound response
        httpNotFound = "HTTP/1.0 404 Not Found\r\n"
        connectionSocket.send(httpNotFound.encode())
        
        # Close the socket
        connectionSocket.close()

serverSocket.close()