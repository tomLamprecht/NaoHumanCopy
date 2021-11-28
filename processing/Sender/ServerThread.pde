import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.InputStreamReader;

class ServerThread extends Thread{

@Override
public void run(){
    ServerSocket ss = null;
      try{
      ss = new ServerSocket(PORT);
    while(true){
       println("SERVER: Server started. Waiting for Connection...");
       Socket socket = ss.accept();
       println("SERVER: Connection with: " + socket);
       ConnectionThread ct = new ConnectionThread(socket);
       ct.start();
    }
      
     } catch(IOException e) {
          e.printStackTrace();
    }
    finally{
          try{
        ss.close();
          }catch(Exception e){
          e.printStackTrace();
          }
    }


}

}