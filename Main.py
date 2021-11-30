import json
import os
from threading import Thread
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

def calculateJoints(x,y,z):
    #Calculating Shoulder Roll
    y = -y
    if(z >= 0):
        angleShoulderPitch = y*90
        angleShoulderRoll =-x*90
    else:
        angleShoulderPitch = y*90 + 2*(-90 - y*90)
        angleShoulderRoll =-x*90
        if(-y < 0):
            angleShoulderPitch = y*90 + 2*(90 - y*90)
            pass

    print(angleShoulderPitch)
    return [radians(angleShoulderPitch), radians(angleShoulderRoll)]


def main():
    startServer()
    socket = Reciever.connectToServer()
    print("CLIENT: Connected to the Server")

    session = qi.Session()

    PORT = 9559
    robotIP = "192.168.178.93"

    session.connect("192.168.178.93:9559")
    motionProxy = ALProxy("ALMotion", robotIP, PORT)

    chainName = "Arms"
    enable  = True
    isSuccess = motionProxy.setCollisionProtectionEnabled(chainName, enable)
    print ("Anticollision activation on Arms: " + str(isSuccess))



  #  print(Reciever.getDataFromServer(socket))
    while(True):
        data = Reciever.getDataFromServer(socket)
        if (data != json.loads("{}")):
            names = ["RShoulderPitch", "RShoulderRoll"]
            x = data["Right_Hand"]["x"]
            y = data["Right_Hand"]["y"]
            z = data["Right_Hand"]["z"]
            angles = calculateJoints(x,y,z)
            maxSpeed = 0.2
            motionProxy.setAngles(names, angles, maxSpeed)

            names = ["LShoulderPitch", "LShoulderRoll"]
            x = data["Left_Hand"]["x"]
            y = data["Left_Hand"]["y"]
            z = data["Left_Hand"]["z"]
            angles = calculateJoints(x,y,z)
            maxSpeed = 0.2
            motionProxy.setAngles(names, angles, maxSpeed)





if __name__ == "__main__":
    main()
