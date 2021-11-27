

//This is the JsonObject that gets send if the client sends a request
JSONObject jsonObject = new JSONObject();

//PORT to Connect to Server
final int PORT = 5001;

void setup() {
startServer();
size(600,700);
}

void draw(){


}

void mousePressed(){
  jsonObject = new JSONObject();
  jsonObject.setString("mouseLocation" + jsonObject.size(), mouseX + " " + mouseY);
}



void startServer(){
  ServerThread st = new ServerThread();
  st.start();
}