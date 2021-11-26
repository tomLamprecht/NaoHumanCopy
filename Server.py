import socket
import sys
import struct

HOST = "localhost"
PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def getLengthOfCommingData(sock):
    alldata = 0
    while True:
        data = sock.recv(100)
        if(len(data) != 0):
            alldata = int(data)
        if(alldata > 0):
            break
    return alldata

def recieveData(sock):
    lengthOfData = getLengthOfCommingData(sock)
    print("Length of Comming Message is: " + str(lengthOfData))
    amount_received = 0
    alldata = ""
    while True:
        data = sock.recv(16)
        alldata += data
        amount_received += len(data)
        #print >>sys.stderr, 'received "%s"' % data
        if(amount_received >= lengthOfData):
            break
    return alldata


try:
    
    # Send data
    message = 'This is the message.  It will be repeated.\n'
    print >>sys.stderr, 'sending: %s' % message
    sock.sendall(message)
    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    print(recieveData(sock))
        

    


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()