import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.InputStreamReader;

JSONObject jsonObject = new JSONObject();
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