import socket
import sys
import json
import time

HOST = "localhost"
PORT = 5001

def connectToServer():
    tries = 10
    for i in range(0, tries):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            return sock
        except Exception as e:
            #wait one secound and try again
            print("CLIENT: Couldnt Connect trying again... (" + str(tries - i) + " tries left)")
            time.sleep(1)

def parseJsonStringToDict(jsonString):
    try:
        return json.loads(jsonString)
    except Exception as e:
        raise Exception("CLIENT: The send Data wasnt in JSON Format.")
        

def getLengthOfCommingData(sock):
    alldata = 0
    while True:
        data = sock.recv(100)

        if(len(data) != 0):
            alldata = int(data)

        if(alldata != 0):
            break
    sock.sendall("\n")
    return alldata

def recieveData(sock):
    lengthOfData = getLengthOfCommingData(sock)
    #print("CLIENT: Length of Comming Message is: " + str(lengthOfData))
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

def getDataFromServer(sock):
    request = '\n'
    sock.sendall(request)
    #print("CLIENT: Request send")
    return recieveData(sock)

