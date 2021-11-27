import socket
import sys
import json
import time

HOST = "localhost"
PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def parseJsonStringToDict(jsonString):
    try:
        return json.loads(jsonString)
    except Exception as e:
        raise Exception("The send Data wasnt in JSON Format.")
        

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
    return parseJsonStringToDict(alldata)


try:
    
    # Send 
    request = '\n'
    sock.sendall(request)
    # Look for the response    
    result = recieveData(sock)
    print(result)

    


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()