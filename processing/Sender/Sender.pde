import kinect4WinSDK.Kinect;

//This is the JsonObject that gets send if the client sends a request
JSONObject jsonObject = new JSONObject();

//PORT to Connect to Server
final int PORT = 5001;

//The Handler for the Kinect Camera
KinectHandler kinectHandler;

void setup() {
startKinect();
startServer();
//the Resolution of the Camera
size(640,480);
smooth();
}

void draw(){
  background(0);
kinectHandler.drawImages();
jsonObject = kinectHandler.getJsonOfLatestBody();
}

void startKinect(){
Kinect kinect =new Kinect(this);
kinectHandler = new KinectHandler(kinect);

}

void startServer(){
  ServerThread st = new ServerThread();
  st.start();
}