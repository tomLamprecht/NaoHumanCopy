import java.util.*;
import kinect4WinSDK.SkeletonData;

class KinectHandler{

  Kinect kinect;
  ArrayList<SkeletonData> bodies;
  boolean calibrated, calibrationInProgress;
  float leftArmMaxDist_x, leftArmMaxDist_y, leftArmMaxDist_z, rightArmMaxDist_x, rightArmMaxDist_y, rightArmMaxDist_z;
  
  class CalibrationThread extends Thread{
    @Override
    public void run(){
        calibrateMethod();
    }
  }
  
  
  public KinectHandler(Kinect kinect) {
  this.kinect =  kinect;
  bodies = new ArrayList<SkeletonData>();
  calibrated = false;  
  
}
  
  public JSONObject getJsonOfLatestBody(){
    //Calculate the coordinates
    Map<String, Float[]> valueMap = calculateCoordinates();
   
   // parse the Coordinates to JSON and return it
   return JsonManager.parseSkeletonToJson(valueMap);  
}


  /**
  * Gives back an Map with a description of a joint as the key, 
  * and as value an array of Integer with the first element beeing the index of the calculating joint
  * and the second element beeing the index of the joint thats the reference point to the calculating joint.
  *
  * To calculate a new joint just add a new entry to the indexMap. 
  * (Warning: Be careful what joint you give as reference point, not all of them have been calibrated to work as intended)
  */
  public Map<String, Integer[]> createIndexMap(){
    Map<String, Integer[]> indexMap = new HashMap<String, Integer[]>();
   indexMap.put("Left_Hand", new Integer[]{Kinect.NUI_SKELETON_POSITION_HAND_LEFT, Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT});
   indexMap.put("Left_Elbow", new Integer[]{Kinect.NUI_SKELETON_POSITION_ELBOW_LEFT, Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT});
   indexMap.put("Right_Hand",new Integer[]{ Kinect.NUI_SKELETON_POSITION_HAND_RIGHT, Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT});
   indexMap.put("Right_Elbow", new Integer[]{Kinect.NUI_SKELETON_POSITION_ELBOW_RIGHT, Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT});
  
   return indexMap;
  }
  
  void drawImages(){
    image(kinect.GetImage(), 320, 0, 320, 240);
  image(kinect.GetDepth(), 320, 240, 320, 240);
  image(kinect.GetMask(), 0, 240, 320, 240);
  drawBody();
}
  
void drawBody(){
  for(SkeletonData body : bodies){
  
    //Draw Right Arm 1
      DrawBone(body, Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT, Kinect.NUI_SKELETON_POSITION_ELBOW_RIGHT);
    
    // Draw Right Arm 2
      DrawBone(body, Kinect.NUI_SKELETON_POSITION_ELBOW_RIGHT, Kinect.NUI_SKELETON_POSITION_WRIST_RIGHT);
  
    //Draw Left Arm 1
      DrawBone(body, Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT, Kinect.NUI_SKELETON_POSITION_ELBOW_LEFT);
   
    //Draw Left Arm 2
      DrawBone(body, Kinect.NUI_SKELETON_POSITION_ELBOW_LEFT, Kinect.NUI_SKELETON_POSITION_WRIST_LEFT);
    
    //Draw Spine 1
      DrawBone(body, Kinect.NUI_SKELETON_POSITION_SHOULDER_CENTER, Kinect.NUI_SKELETON_POSITION_SPINE);
    
    //Draw Spine 2
      DrawBone(body, Kinect.NUI_SKELETON_POSITION_HIP_CENTER, Kinect.NUI_SKELETON_POSITION_SPINE);
 }  
    
  }




  void DrawBone(SkeletonData _s, int _j1, int _j2) 
  {
    noFill();
    stroke(255, 255, 0);
    if (_s.skeletonPositionTrackingState[_j1] != Kinect.NUI_SKELETON_POSITION_NOT_TRACKED &&
      _s.skeletonPositionTrackingState[_j2] != Kinect.NUI_SKELETON_POSITION_NOT_TRACKED) {
      line(_s.skeletonPositions[_j1].x*width/2, 
      _s.skeletonPositions[_j1].y*height/2, 
      _s.skeletonPositions[_j2].x*width/2, 
      _s.skeletonPositions[_j2].y*height/2);
    }
    text( _s.skeletonPositions[_j2].z, width/2, height/2);
  }
  
  
  public void calibrate(){
    if(!calibrationInProgress){
      new CalibrationThread().start();
    }else{
      println("Already Calibrating right now");
    }
  }
  
  private void calibrateMethod(){
    calibrated = false;
    calibrationInProgress = true;
    
   //Get latest Registered Body
   if(bodies.size() < 1){
     println("No Bodies tracked... couldnt calibrate");
     calibrationInProgress = false;
     return;
   }
   SkeletonData body = bodies.get(bodies.size()-1);
  
   //Calibrate X Values
   if(!calibrationPreparation("Reach out both arms sideways", body)) return;
   this.leftArmMaxDist_x =abs(body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_HAND_LEFT].x - body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT].x);
   this.rightArmMaxDist_x = abs(body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_HAND_RIGHT].x  - body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT].x);
   println("X Values calibrated");
   
   //Calibrate Y Values
   if(!calibrationPreparation("Put up both arms", body)) return;
   this.leftArmMaxDist_y = abs(body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_HAND_LEFT].y - body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT].y);
   this.rightArmMaxDist_y = abs(body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_HAND_RIGHT].y  - body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT].y);
   println("Y Values calibrated");
   
   //Calibrate Z Values
   if(!calibrationPreparation("Reach both arms infront of you", body)) return;
   this.leftArmMaxDist_z = abs(body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_HAND_LEFT].z - body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT].z);
   this.rightArmMaxDist_z = abs(body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_HAND_RIGHT].z  - body.skeletonPositions[Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT].z);
   println("Z Values calibrated");
   
   calibrated = true;
   calibrationInProgress = false;
}

  /**
  *This Method does the preparation for each calibration step and returns false if the body is no longer tracked
  */
  private boolean calibrationPreparation(String output, SkeletonData body){
     println(output);
     printCountDown(5);
     if(!isBodyTracked(body)){
       print("Person couldnt be tracked anymore. Canceling Calibration");
       calibrated = false;
       calibrationInProgress = false;
       return false;
     }
     return true;
  }
  
  public boolean isBodyTracked(SkeletonData body){
    return (body.trackingState == Kinect.NUI_SKELETON_TRACKED);
  }
  
  private void printCountDown(int duration){
       for(int i = 0; i < duration; i++){
     try{
       println(i);
       Thread.sleep(1000);
     }catch(InterruptedException e) {
       e.printStackTrace();
     }
   }
  }
    public Map<String, Float[]> calculateCoordinates(){
    if(bodies.size() < 1) return null;
    
      //Get latest Registered Body
      SkeletonData body = bodies.get(bodies.size()-1);
            
      if(body.trackingState == Kinect.NUI_SKELETON_POSITION_NOT_TRACKED || !calibrated)
        return null;

      Map<String, Float[]> valueMap = new HashMap<String, Float[]>();
      Map<String, Integer[]> indexMap = createIndexMap();
      for(String keyElement : indexMap.keySet()){
            Integer[] indexes = indexMap.get(keyElement);
            float x = body.skeletonPositions[indexes[0]].x - body.skeletonPositions[indexes[1]].x;
            float y = -(body.skeletonPositions[indexes[0]].y - body.skeletonPositions[indexes[1]].y);
            float z = -(body.skeletonPositions[indexes[0]].z - body.skeletonPositions[indexes[1]].z);
            x = mapDistToPercentage(x, leftArmMaxDist_x);
            y  = mapDistToPercentage(y, leftArmMaxDist_y);
            z = mapDistToPercentage(z, leftArmMaxDist_z);
            valueMap.put(keyElement, new Float[]{x,y,z});
      }
      return valueMap;
    }
  
  
  public float mapDistToPercentage(float realDist, float maxDist){
    return limitValue(map(realDist, -maxDist, maxDist, -1, 1),-1, 1);
  }
  
  public float limitValue (float value, float min, float max){
  if(value < min) return min;
  else if(value > max) return max;
  return value;
  }
  
 
  
  
}

void appearEvent(SkeletonData _s) 
{
  if (_s.trackingState == Kinect.NUI_SKELETON_NOT_TRACKED) 
  {
    return;
  }
  synchronized(kinectHandler.bodies) {
    kinectHandler.bodies.add(_s);
  }
}

void disappearEvent(SkeletonData _s) 
{
  synchronized(kinectHandler.bodies) {
    for (int i=kinectHandler.bodies.size ()-1; i>=0; i--) 
    {
      if (_s.dwTrackingID == kinectHandler.bodies.get(i).dwTrackingID) 
      {
        kinectHandler.bodies.remove(i);
      }
    }
  }
}

void moveEvent(SkeletonData _s, SkeletonData _s2){
//Not yet implemented;
}