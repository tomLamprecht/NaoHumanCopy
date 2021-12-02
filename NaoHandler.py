from naoqi import ALProxy
import json
from math import pi, radians
from math import degrees
import numpy as np

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

            names = ["LElbowRoll"]
            xE = data["Left_Elbow_HR"]["x"]
            yE = data["Left_Elbow_HR"]["y"]
            zE = data["Left_Elbow_HR"]["z"]
            xH = data["Left_Hand"]["x"]
            yH = data["Left_Hand"]["y"]
            zH = data["Left_Hand"]["z"]

            angles = self.calculateJointsHand(xE,yE,zE, xH, yH, zH)
            maxSpeed = 0.2
            self.motionProxy.setAngles(names,angles, maxSpeed)

            names = ["RElbowRoll"]
            xE = data["Right_Elbow_HR"]["x"]
            yE = data["Right_Elbow_HR"]["y"]
            zE = data["Right_Elbow_HR"]["z"]
            xH = data["Right_Hand"]["x"]
            yH = data["Right_Hand"]["y"]
            zH = data["Right_Hand"]["z"]

            angles = self.calculateJointsHand(xE,yE,zE, xH, yH, zH)
            maxSpeed = 0.2
            self.motionProxy.setAngles(names,angles, maxSpeed)

    def getVector(self, x1,y1,z1, x2,y2,z2):
        return (x2-x1, y2-y1, z2-z1)


    def unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def angle_between(self, v1, v2):
        # Returns the angle in radians between vectors 'v1' and 'v2'::
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


    def calculateJointsHand(self, xE,yE,zE, xH, yH, zH):
        elbowToHandVec = self.getVector(xE,yE,zE, xH,yH,zH)
        elbowToShoulder = self.getVector(xE,yE,zE, 0,0,0)
        angle = self.angle_between(elbowToHandVec, elbowToShoulder)-pi
        return [angle]

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




