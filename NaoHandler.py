from naoqi import ALProxy
import json
from math import radians

class NaoHandler:


    def  __init__(self, robotIP):
        self.PORT = 9559
        self.robotIP = robotIP
        self.motionProxy = ALProxy("ALMotion", self.robotIP, self.PORT)
        self.enableCollisionProtection(self.motionProxy)


    def enableCollisionProtection(self, motionProxy):
        chainName = "Arms"
        enable  = True
        isSuccess = motionProxy.setCollisionProtectionEnabled(chainName, enable)
        print ("Anticollision activation on Arms: " + str(isSuccess))

    def moveJoints(self, data):
         if (data != json.loads("{}")):
            names = ["RShoulderPitch", "RShoulderRoll"]
            x = data["Right_Elbow"]["x"]
            y = data["Right_Elbow"]["y"]
            z = data["Right_Elbow"]["z"]
            angles = self.calculateJoints(x,y,z)
            maxSpeed = 0.2
            self.motionProxy.setAngles(names, angles, maxSpeed)

            names = ["LShoulderPitch", "LShoulderRoll"]
            x = data["Left_Elbow"]["x"]
            y = data["Left_Elbow"]["y"]
            z = data["Left_Elbow"]["z"]
            angles = self.calculateJoints(x,y,z)
            maxSpeed = 0.2
            self.motionProxy.setAngles(names, angles, maxSpeed)

    def calculateJoints(self, x,y,z):
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

        return [radians(angleShoulderPitch), radians(angleShoulderRoll)]




