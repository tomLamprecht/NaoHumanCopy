import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.InputStreamReader;


ServerSocket ss;
final int PORT = 5001;

void setup() {
    try{
       ss = new ServerSocket(PORT);
    
       println("Waiting for Connection...");
       Socket socket = ss.accept();
       println("Connection with: " + socket);
       OutputStream os = socket.getOutputStream();
       InputStream is = socket.getInputStream();
       BufferedReader br = new BufferedReader(new InputStreamReader(is));
       BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(os));
        String line = br.readLine();
       println(line);
      // bw.write("This is the Answer");
      // bw.flush();
        os.write(1234567);
         os.flush();
       os.close();
       is.close();
      println("Server Closed");
      exit();
      
} catch(IOException e) {
        e.printStackTrace();
}
}

void draw() {
    background(255,0,0);
}