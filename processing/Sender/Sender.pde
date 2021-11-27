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
    while(true){
       println("Waiting for Connection...");
       Socket socket = ss.accept();
       println("Connection with: " + socket);
       OutputStream os = socket.getOutputStream();
       InputStream is = socket.getInputStream();
       BufferedReader br = new BufferedReader(new InputStreamReader(is));
       BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(os));
        String line = br.readLine();
       println(line);
        JSONObject json = new JSONObject();
        for(int i = 0 ; i < 10; i++)
        json.setString("key" + i, "value" + i);

        sendData(json,bw, br);
       os.close();
       is.close();
    }
      
} catch(IOException e) {
        e.printStackTrace();
}
}

void sendData(JSONObject jsonObject, BufferedWriter bw, BufferedReader br) throws IOException{
  String parsedJson = jsonObject.toString(); 
  int messageLength = parsedJson.length();
  bw.write(String.valueOf(messageLength));
   bw.flush();
   println("Length of Message Send, waiting for confirmation...");
   br.readLine();
   println("Length got confirmed, sending JSON...");
  bw.write(parsedJson); 
  bw.flush();
  println("Data send");
}