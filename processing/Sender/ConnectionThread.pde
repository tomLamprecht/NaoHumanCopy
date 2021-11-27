import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.InputStreamReader;

public class ConnectionThread extends Thread{
  
  Socket socket;
  
  public ConnectionThread(Socket socket){
    this.socket = socket;
  }
  
  @Override
  public void run(){
    OutputStream os = null;
    InputStream is = null;
    try{
       os = socket.getOutputStream();
       is = socket.getInputStream();
       BufferedReader br = new BufferedReader(new InputStreamReader(is));
       BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(os));
       while(true){
         //Wait until Request
         println("Wait until Client sends a Request...");
         br.readLine();
         
         //Create dummy Json
        JSONObject json = new JSONObject();
        for(int i = 0 ; i < 10; i++)
        json.setString("key" + i, "value" + i);
        
        //send JSON
        sendData(json,bw, br);
       }
    }
    catch(IOException e)
    {
      println("Client probably ended the Connection");
    }
    finally{
      try{
        os.close();
        is.close();
      }
      catch(Exception e){
        e.printStackTrace();
      }
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
  println("Data send");
  bw.flush();
}
  
}