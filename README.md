# NaoHumanCopy

---

# Client Server Connection Protokol

The Client is Written in Python and the Server in Java.
The Protokol for the communication is the following:

- **Request**\
        The Client sends a request to the Server

- **Answer**\
        The Server sends 2 messages back. The first gonna be the length of the upcomming JSON and the second is the JSON. (It is assumed that the size of JSON can be saved in a integer (32 Bit))

<br>
This can be repeated as often as necessary.\
The responding JSON has all Coordinates of the 3D Modell.

---

# TO DO

- **Decide on if the Coordinates get parsed in Java or Python**

- **Parse the Coordinates**

- **Write a Function in Java to get the Coordinates in a List**

- **Parse the Coordinates in JSON (Java)**

- **Write a Function in Python for controlling the Robot Arms with parsed Coordinates**

- **Update the Client Server to accept JSON instead of Strings only**

- **Maybe find a solution to find a better performing way to send the length of the upcomming message**\
    Right now this happens with a Storage Usage of 100 Bytes. :/

- **Write a Main Function for the Python Script**