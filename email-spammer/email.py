from socket import *
import base64

# Choose a mail server (e.g. NYU. mail server) and call it mailserver
# > nslookup
# > set type=MX
# > home.nyu.edu
# RESULT: home.nyu.edu MX preference = 10, mail exchanger = mxa-00256a01.gslb.pphosted.com

mailserver = 'mxa-00256a01.gslb.pphosted.com'
serverPort = 25

# Create socket and establish TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))

tcp_resp = clientSocket.recv(1024).decode()
print(tcp_resp)
# Send HELO command to begin SMTP handshake.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
helo_resp = clientSocket.recv(1024).decode()
print(helo_resp)

# Send MAIL FROM command and print response.
mailfromCommand = 'MAIL FROM: <fakeemail@anything.com>\r\n'
clientSocket.send(mailfromCommand.encode())
mailfrom_resp = clientSocket.recv(1024).decode()
print(mailfrom_resp)

# Send RCPT TO command and print server response.
rcpttoCommand = 'RCPT TO: <mlh9655@nyu.edu>\r\n'
clientSocket.send(rcpttoCommand.encode())
rcptto_resp = clientSocket.recv(1024).decode()
print(rcptto_resp)

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
data_resp = clientSocket.recv(1024).decode()
print(data_resp)

# Send email data.
emailLine1 = "Hello there!\r\nThis is the second line of the email.\r\n"
clientSocket.send(emailLine1.encode())
emailLine2 = "Aaaaand here's the third!\r\n"
clientSocket.send(emailLine2.encode())

# Send message to close email message.
emailEnd = ".\r\n"
clientSocket.send(emailEnd.encode())

# Send QUIT command and get server response.
quitCommand = "QUIT\r\n"
clientSocket.send(quitCommand.encode())
serv_resp = clientSocket.recv(1024).decode()
print(serv_resp)



clientSocket.close()