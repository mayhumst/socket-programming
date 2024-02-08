from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii

# Don’t worry about this method
def checksum(str):
    csum = 0
    countTo = (len(str) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = str[count+1] * 256 + str[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(str):
        csum = csum + ord(str[len(str) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        timeStart = time.time()
        select.select([mySocket], [], [], timeLeft)
        timeLeft = (time.time() - timeStart) #HERE QUESTION: new variable????
        timeReceived = time.time()

        # Receive the packet and address from the socket
        rec_packet, addr = mySocket.recvfrom(1024)

        # Extract the ICMP header from the IP packet
        icmp_header = rec_packet[20:28]

        # Use struct.unpack to get the data that was sent via the struct.pack method below
        type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)

        # Verify Type/Code is an ICMP echo reply
        if type != 0: #QUESTION HERE: 8 or 0
            if code != 0:
                return "error"

        # Extract the time in which the packet was sent
        bytesInDouble = struct.calcsize("d")
        timeSent = struct.unpack("d", rec_packet[28:28 + bytesInDouble])[0]

        # Return the delay (time sent - time received)
        return timeReceived - timeSent #QUESTION HERE: WHICH ORDER

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0

    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    
    # Define icmpEchoRequestType and icmpEchoRequestCode, which are both used below
    icmpEchoRequestType = 8
    icmpEchoRequestCode = 0

    header = struct.pack("bbHHh", icmpEchoRequestType, icmpEchoRequestCode, myChecksum, ID, 1)
    
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack("bbHHh", icmpEchoRequestType,icmpEchoRequestCode, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str

def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")
    #SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.ord/papers/sock_raw

    #Create Socket here
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    #Fill in end

    myID = os.getpid() & 0xFFFF #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    #timeout=1 means: If one second goes by without a reply from the server,
    #the client assumes that either the client's ping or the server's pong is lost
    dest = socket.gethostbyname(host)
    print ("Pinging " + dest + " using Python:\n")
    #Send ping requests to a server separated by approximately one second
    while 1 :
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)# one second
    return delay

ping("nytimes.com")