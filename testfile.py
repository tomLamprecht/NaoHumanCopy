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

print(motionProxy.getBodyNames("Body"))
names = ["RElbowRoll"]
angles = (radians(-90))
maxSpeed = 0.2
motionProxy.setAngles(names, angles, maxSpeed)