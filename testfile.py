import qi
from naoqi import ALProxy
from math import radians

session = qi.Session()

PORT = 9559
robotIP = "192.168.178.93"

session.connect("192.168.178.93:9559")
motionProxy = ALProxy("ALMotion", robotIP, PORT)

shoulder = {"x":0.5,"y":0.3,"z":1000}
ellbow = {"x":0.4, "y":0.4,"z":1200}




print(motionProxy.getBodyNames("Body"))
names = ["RShoulderPitch"]
angles = [radians(-119)]
maxSpeed = 0.2
motionProxy.setAngles(names, angles, maxSpeed)
a = raw_input("")