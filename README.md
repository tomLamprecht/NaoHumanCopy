# READ ME for the NaoHumanCopy

---

**Version ALPHA**
---

![Python 2.7, 3.7](https://img.shields.io/badge/Python-2.7%2C%203.7-3776ab.svg?maxAge=2592000)


Only tested on Nao V6

---

# Overview

This is a basic program that copies the movement of a human with nao, with the help of a Kinect camera. This is meant to be a show performance programm, there are <u><b>no</b></u> methods or classes that are meant to be used outside of this programm.

- [Usage](#usage)
    - [Start the Program](#start-program) 

- [Installation Guide](#install-guide)

- [Client Server Connection Protocol](#connection-protocol)

- [License & Copyright](#license)

<br>

---

<a name="usage"></a>

# Usage

<a name="start-program"></a>

## Start the Program

First you have to direct to the folder where the files are located\
then you have to run following command in your console:

```
c:/Python27/python.exe Main.py
```

*(if your python2.7 executeable is located somewhere else, just change the path to the matching location)*
<br>


## Program schedule


The Program schedule can be split up in 3 different sections:

 - **Booting:**\
        The program boots up. The Server tries to connect with the Kinect camera and the Python client builds up a connection with the Server.

 - **Configuration:**
        The program has sucesfully booted up and is ready to be configurated.<br/> For configuration stand in front of the camera and wait for the program to detect your sceleton. Then press the ```space``` button and followe the steps on the screen.
       
    * &ensp; Arms straight up
    * &ensp; Arms to the left
    * &ensp; Arms infront of u

 - **Running:**\
         The program is now configurated and ready to use. Nao should now copy every moment of the person he is watching.


---

<a name="install-guide"></a>

# Installation Guide


Following Python versions with matching Libraries have to be installed.
<br>

- ## Python 2.7 ([Download](https://www.python.org/download/releases/2.7/))
    **Libraries:**\
    <u>PIP dropped the support for Python 2 in January 2021, therfore all Libraries for Python 2.7 have to be installed manuelly</u>

    * &ensp;[naoqi Python SDK](https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-2.1.4.13.win32.exe)
   
- ## Processing ([Download](https://processing.org/download))
    **Libraries:**

    * &ensp;[Kinect4WinSDK](https://github.com/chungbwc/Kinect4WinSDK)



---
<a name="connection-protocol"></a>
# Client Server Connection Protocol
<u> This section is only helpful for development and not required for running the program</u>

The client is written in Python and the server in Java.
The protocol for the communication is the following:

- **Request**\
        The client sends a request to the server

- **Answer**\
        The server sends the length of the upcomming JSON. (It is assumed that the size of JSON can be saved in a integer (32 Bit))

- **Confirmation**\
        The client has to read the first Message and send an confirmation back to the server that he is ready for the JSON

- **Final Answer**\
        The server sends the JSON and is ready for the next connection 

<br>
This can be repeated as often as necessary.<br/>
The responding JSON has all coordinates of the 3D modell.

---



<a name="license"></a>

# License & copyright

© Tom Lamprecht, FHWS Fakultät Informatik
