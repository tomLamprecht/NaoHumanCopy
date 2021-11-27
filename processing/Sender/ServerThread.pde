class ServerThread extends Thread{

@Override
public void run(){
    ServerSocket ss = null;
      try{
      ss = new ServerSocket(PORT);
    while(true){
       println("Waiting for Connection...");
       Socket socket = ss.accept();
       println("Connection with: " + socket);
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