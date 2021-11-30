import qi
from naoqi import ALProxy
from math import radians

session = qi.Session()

PORT = 9559
robotIP = "192.168.178.93"

session.connect("192.168.178.93:9559")
motionProxy = ALProxy("ALMotion", robotIP, PORT)

ellbow = {"x":0.4, "y":0.4,"z":0.3}

# Example showing how to activate "Arms" anticollision
chainName = "Arms"
enable  = True
isSuccess = motionProxy.setCollisionProtectionEnabled(chainName, enable)
print ("Anticollision activation on Arms: " + str(isSuccess))


def calculateJoints():
    #Calculating Shoulder Roll
    x = 0
    y = -0.8
    y = -y
    z = -1
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

print(motionProxy.getBodyNames("Body"))
names = ["RShoulderPitch", "RShoulderRoll"]
angles = calculateJoints()
maxSpeed = 0.2
motionProxy.setAngles(names, angles, maxSpeed)