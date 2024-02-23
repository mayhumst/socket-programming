# socket-programming

*Socket programming, TCP, IP, HTTP, ICMP, SMTP, computer networking*

---

This repository contains a few small examples of socket programming utilizing different protocols. 

---

## Traceroute -- IP, ICMP

*May 2023*

This program allows the user to trace the route from the host running the program to any other host in the world using ICMP ping messages. 

The program sends ICMP echo (ICMP type '8') messages to the destination with increasing Time To Live values. The routers along the path will return ICMP Time Exceeded (type '11') messages when TTL becomes 0. The final destination returns ICMP Reply (type '0') upon receiving the echo request. The IP addresses of the routers along the path can then be extracted from the received packets. To determine round-trip time between the host and any router, the timer should be set at the host. 

## Pinger -- IP, ICMP

*May 2023*

This program contains an implementation of Ping, used to determine whether a particular host is reachable across an IP network. This works by sending ICMP echo reply packets to the target host and listening for ICMP echo reply packets. Ping measures the round-trip time, records packet loss, and prints a statistical summary of the echo reply packets received. 

This program sends ping requests to the host once every second, using packets with data payloads containing a timestamp. The application will wait one second for a reply. If no reply is recieved, the program assumes a packet was lost or the server is down. 

## Web Server -- TCP, HTTP

*February 2023*

This program creates a simple HTTP web server that will do the following: 

1. Accept and parse an incoming HTTP request for a file
2. Get the content of the file from the server's local file system
3. Create an HTTP OK response with a cookie to be set in the response headers and the content of the file
4. Return a HTTP NotFound response if the requested file does not exist

## Email Spammer -- TCP, SMTP 

*February 2023*

This program implements a simple mail client by establishing a TCP connection, performing an SMTP handshake, sending a message, and terminating the connection. This program does NOT use the Python module smtplib. 

To adapt this program to change the email body message or the sender's email address, change the code in the marked places. The body can contain any message. The sender email address can be any address, existing or non-existing, but should follow proper email address format. To change the recipient's email address, follow these instructions to change the mail server. 

1. Open your terminal. In Windows, enter the command nslookup. (For MacOS, the command is dig.)
2. Enter the command type=mx to set the type of server lookup to mail exchanger. 
3. Enter the domain address of the email's domain. (In my program, I used an NYU email address, so I entered home.nyu.edu)
4. Look for the domain of a mail exchanger, likely with an MX preference = 10 or similar. 
5. Replace the recipient's email address with the address you chose, and replace the mail server with the domain found in step 4. 

**Note: some email servers do not accept TCP connections from unknown addresses, so not all email domains will work as a valid recipient.**
