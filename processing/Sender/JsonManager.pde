import kinect4WinSDK.SkeletonData;

public static class JsonManager{

  
    public static JSONObject parseSkeletonToJson(Map<String, Float[]> valueMap){
            JSONObject json = new JSONObject();
            
            //if the valueMap is invalid return the emptyJson
            if(valueMap == null)
                return json;
            
            //get the Names of all calculated Coordinates
            Set<String> keys = valueMap.keySet();
           //Build the JSON
           for(String element : keys){
             JSONObject temp = new JSONObject();
             Float[] pos = valueMap.get(element);
             temp.setDouble("x",pos[0]);
             temp.setDouble("y", pos[1]);
             temp.setDouble("z", pos[2]);
             json.setJSONObject(element,temp);
           }
          return json;
    }

}