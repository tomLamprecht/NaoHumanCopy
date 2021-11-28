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
    counter = 0
    timeCurrent = time.time()
    while(time.time() <= (timeCurrent +1)):
        Reciever.getDataFromServer(socket)
        counter = counter + 1
    print(str(counter) + " Abfragen pro Sekunde")

if __name__ == "__main__":
    main()
