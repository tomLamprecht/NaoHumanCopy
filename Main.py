import json
import os
from threading import Thread
from NaoHandler import NaoHandler
import Reciever
import time
import qi
from naoqi import ALProxy
from math import radians



def bootServer():
    currentDir = os.path.abspath(os.getcwd())
    print("compiling Server")
    os.system('processing-java --platform=windows --sketch="' + currentDir+ '\processing\Sender" --force --run')

def startServer():
    t = Thread(target = bootServer)
    t.start()


def calculateJointsElbow(x,y,z):
    #Not Implemented yet
    pass







def main():
    startServer()
    socket = Reciever.connectToServer()
    print("CLIENT: Connected to the Server")
    nao = NaoHandler("192.168.178.93")


  #  print(Reciever.getDataFromServer(socket))
    while(True):
        data = Reciever.getDataFromServer(socket)
        nao.moveJoints(data)





if __name__ == "__main__":
    main()
