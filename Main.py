import os
from threading import Thread
import Reciever
import time

def bootServer():
    currentDir = os.path.abspath(os.getcwd())
    print("compiling Server")
    os.system('processing-java --platform=windows --sketch="' + currentDir+ '\processing\Sender" --force --run')

def startServer():
    t = Thread(target = bootServer)
    t.start()

def main():
    startServer()
    socket = Reciever.connectToServer()
    print("CLIENT: Connected to the Server")
  #  print(Reciever.getDataFromServer(socket))
    while(True):
        time.sleep(1)
        print(Reciever.getDataFromServer(socket))

if __name__ == "__main__":
    main()
