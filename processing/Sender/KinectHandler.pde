import java.util.*;
import kinect4WinSDK.SkeletonData;

class KinectHandler{

  Kinect kinect;
  ArrayList<SkeletonData> bodies;
  
  public KinectHandler(Kinect kinect) {
  this.kinect =  kinect;
  bodies = new ArrayList<SkeletonData>();
  }
  
  public JSONObject getJsonOfLatestBody(){
    //If no Body is registered, return empty JSON
    if(bodies.size() == 0)
      return new JSONObject();
      
    //Get Latest Body
    SkeletonData currentBody = bodies.get(bodies.size()-1);
    
    // If current body isnt tracked return empty JSON
   if( currentBody.trackingState == Kinect.NUI_SKELETON_POSITION_NOT_TRACKED){
     return new JSONObject();
   }

    //Get an Map of all Coordinates that have to be tracked
   Map<String, Integer> indexMap = createIndexMap();
   
   // build and return the JSONObject
   return JsonManager.parseSkeletonToJson(indexMap, currentBody);
  }
  
  public Map<String, Integer> createIndexMap(){
    Map<String, Integer> indexMap = new HashMap<String, Integer>();
   indexMap.put("Left_Shoulder", Kinect.NUI_SKELETON_POSITION_SHOULDER_LEFT);
   indexMap.put("Left_Elbow", Kinect.NUI_SKELETON_POSITION_ELBOW_LEFT);
   indexMap.put("Left_Wrist", Kinect.NUI_SKELETON_POSITION_WRIST_LEFT);
   indexMap.put("Right_Shoulder", Kinect.NUI_SKELETON_POSITION_SHOULDER_RIGHT);
   indexMap.put("Right_Elbow", Kinect.NUI_SKELETON_POSITION_ELBOW_RIGHT);
   indexMap.put("Right_Wrist", Kinect.NUI_SKELETON_POSITION_WRIST_RIGHT);
  
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