# NaoHumanCopy

---

# Client Server Connection Protokol

The Client is Written in Python and the Server in Java.
The Protokol for the communication is the following:

- **Request**\
        The Client sends a request to the Server

- **Answer**\
        The Server sends the length of the upcomming JSON. (It is assumed that the size of JSON can be saved in a integer (32 Bit))

- **Confirmation**\
        The Client has to read the first Message and send an confirmation back to the Server that he is ready for the JSON

- **Final Answer**\
        The Server sends the JSON and is ready for the next Connection 

<br>
This can be repeated as often as necessary.\
The responding JSON has all Coordinates of the 3D Modell.

---

# TO DO

- **Angel Calculation of Elbow: **
-> Ebene Aufspannen mit 0 Punkt, Elbow Coordinate und Elbow Coordinate mit negativen x-Value. Winkel von Vector(Elbow to Hand) zur Ebene Berechnen. Das sollte der gesuchte Winkel sein.
