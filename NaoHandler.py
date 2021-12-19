import math
from naoqi import ALProxy
import json
from math import pi, radians
from math import degrees
import numpy as np
import time

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
            angles = self.repairAngles(angles)
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
            angles = self.repairAngles(angles)
            self.motionProxy.setAngles(names,angles, maxSpeed)


            names = ["LElbowYaw"]
            xE = data["Left_Elbow_HR"]["x"]
            yE = data["Left_Elbow_HR"]["y"]
            zE = data["Left_Elbow_HR"]["z"]
            xH = data["Left_Hand"]["x"]
            yH = data["Left_Hand"]["y"]
            zH = data["Left_Hand"]["z"]

            angles = self.calculateJointsElbowYaw(xE,yE,zE, xH, yH, zH)
            angles = self.repairAngles(angles)
            maxSpeed = 0.2
            print(angles)
            self.motionProxy.setAngles(names,angles, maxSpeed)

            names = ["RElbowYaw"]
            xE = data["Right_Elbow_HR"]["x"]
            yE = data["Right_Elbow_HR"]["y"]
            zE = data["Right_Elbow_HR"]["z"]
            xH = data["Right_Hand"]["x"]
            yH = data["Right_Hand"]["y"]
            zH = data["Right_Hand"]["z"]

            angles = self.calculateJointsElbowYaw(xE,yE,zE, xH, yH, zH)
            maxSpeed = 0.2
            angles = self.repairAngles(angles)
           # self.motionProxy.setAngles(names,angles, maxSpeed)

    def repairAngles(self, angles):
        if (math.isnan(angles[0])):
            return (0)
        return (angles[0])

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

    def calculateJointsElbowYaw(self, xE, yE, zE, xH, yH, zH):
        p1 = (xE, yE, zE)
        p2 = (xH, yH, zH)
        p3 = (-xE, yE, zE)
        zero = (0,0,0)
        p4 = add_v3v3(np.cross(p1,p3), p2)
        intersection = isect_line_plane_v3(p2,p4,zero ,p4)
        intersection2 = isect_line_plane_v3(zero,p1,intersection, p1)

        between = sub_v3v3(intersection, intersection2)
        p1TOp2 = sub_v3v3(p2, intersection2)
        a = self.angle_between(between, p1TOp2)
        p2c = mul_v3_fl(p2, 100)
        p4c = add_v3v3(np.cross(mul_v3_fl(p1, 100), mul_v3_fl(p3,100)), p2c)

        dist = (p2c[0]*p4c[0] + p2c[1]*p4c[1] + p2c[2]*p4c[2])/math.sqrt(math.pow(p4c[0],2) + math.pow(p4c[1], 2) + math.pow(p4c[2],2) )
        a -=  radians(90)
        if(dist < 0):
            #a -= radians(90)
            pass
        else:
            a *= -1
            pass
            
        return [a]

    # intersection function
def isect_line_plane_v3(p0, p1, p_co, p_no, epsilon=1e-6):
    """
    p0, p1: Define the line.
    p_co, p_no: define the plane:
        p_co Is a point on the plane (plane coordinate).
        p_no Is a normal vector defining the plane direction;
             (does not need to be normalized).

    Return a Vector or None (when the intersection can't be found).
    """

    u = sub_v3v3(p1, p0)
    dot = dot_v3v3(p_no, u)

    if abs(dot) > epsilon:
        # The factor of the point between p0 -> p1 (0 - 1)
        # if 'fac' is between (0 - 1) the point intersects with the segment.
        # Otherwise:
        #  < 0.0: behind p0.
        #  > 1.0: infront of p1.
        try:
            a = p0[0]
            a = p_co[0]
        except Exception as e:
            return None
        w = sub_v3v3(p0, p_co)
        fac = -dot_v3v3(p_no, w) / dot
        u = mul_v3_fl(u, fac)
        return add_v3v3(p0, u)

    # The segment is parallel to plane.
    return (0,0,0)

# ----------------------
# generic math functions

def add_v3v3(v0, v1):
    return (
        v0[0] + v1[0],
        v0[1] + v1[1],
        v0[2] + v1[2],
    )


def sub_v3v3(v0, v1):
    try:
        return (
            v0[0] - v1[0],
            v0[1] - v1[1],
            v0[2] - v1[2],
        )
    except:
        return(0,0,0)


def dot_v3v3(v0, v1):
    return (
        (v0[0] * v1[0]) +
        (v0[1] * v1[1]) +
        (v0[2] * v1[2])
    )


def len_squared_v3(v0):
    return dot_v3v3(v0, v0)


def mul_v3_fl(v0, f):
    return (
        v0[0] * f,
        v0[1] * f,
        v0[2] * f,
    )
        



