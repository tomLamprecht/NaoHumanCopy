import kinect4WinSDK.SkeletonData;

public static class JsonManager{

  
    public static JSONObject parseSkeletonToJson(Map<String, Integer> indexMap, SkeletonData currentBody){
            PVector[] positions = currentBody.skeletonPositions;
            JSONObject json = new JSONObject();
            //Get an Map of all Coordinates that have to be tracked
            Set<String> keys = indexMap.keySet();
           //Build the JSON
           for(String element : keys){
             JSONObject temp = new JSONObject();
             PVector pos = positions[indexMap.get(element)];
             temp.setDouble("x",pos.x);
             temp.setDouble("y", pos.y);
             temp.setDouble("z", pos.z);
             json.setJSONObject(element,temp);
           }
          return json;
    }

}