
package com.emapix;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.security.SecureRandom;
import java.math.BigInteger;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.util.Log;

class ServicePhotoData implements IPhotoData 
{
	private static final String FILE_EXT	= "jpg";
	
	private SecureRandom random = new SecureRandom();
	private Context context;
	
	public ServicePhotoData(Context context) {
		this.context	= context;
	}
	
    public boolean setResource(int res_id, String resource) {
    	// Updates resource data 
		HashMap<String, String> params	= new HashMap<String, String>();
		params.put("resource", resource);
		JSONObject js	= getContentObject(String.format("%s/update", res_id), params);
		try {
			return isSuccess(js.getString("status"));
		} catch (Exception e){
    		Log.e("ServicePhotoData.setResource", e.toString());
    		return false;			
		}    	
    }
    
    public ResourceImage get(int res_id) {
    	// Returns photo request specified by id
    	JSONObject js	= getContentObject(String.format("%s", res_id), null);
    	try {
    		return toResourceImage(js.getJSONObject("result"));
    	} catch (Exception e) {
    		Log.e("ServicePhotoData.get", e.toString());
    		return null;
    	}
    }
    
    public ResourceImage[] getAll() {
    	// Returns all photo requests
		JSONObject js	= getContentObject("all", null);		
		try {
			JSONArray arr	= js.getJSONArray("result");
			ResourceImage[] ri = new ResourceImage[arr.length()];
			for (int i=0; i< arr.length(); i++)
				ri[i]	= toResourceImage(arr.getJSONObject(i));
			
			return ri;
		} catch (Exception e) {
			Log.e("ServicePhotoData.getAll", e.toString());
			return new ResourceImage[0];
		}
    }
    
    public ResourceImage add(int lat, int lon) {
    	// Adds resource image
		HashMap<String, String> params	= new HashMap<String, String>();
		params.put("lat", String.format("%s", lat));
		params.put("lon", String.format("%s", lon));
		params.put("resource", genRes());
		JSONObject js	= getContentObject("add", params);
		try {
			return toResourceImage(js.getJSONObject("result"));
		} catch (Exception e){
    		Log.e("ServicePhotoData.add", e.toString());
    		return null;			
		}
    }
    
    public boolean remove(int res_id) {
    	// Removes record
		JSONObject js	= getContentObject(String.format("%s/remove", res_id), null);
		try {
			return isSuccess(js.getString("status"));
		} catch (Exception e){
    		Log.e("ServicePhotoData.add", e.toString());
    		return false;			
		}    	
    }
    
    public boolean isEmpty(int res_id) {    	
    	return get(res_id) == null;
    }
    
    public int size() {    	
    	return 0;
    }
    
    private boolean isSuccess(String status) {    	
		return status.equals("ok");
    }
    
    private String genRes() {
    	return new BigInteger(130, random).toString(16);
    }
    
    public String getFullUri(String resource) {
    	// Returns full uri of the image
		String base_s3	= context.getString(R.string.base_s3);
		return String.format("%s/%s.%s", base_s3, resource, FILE_EXT);    	
    }
    
    public ResourceImage toResourceImage(JSONObject obj) {
    	// Converts JSON object to ResourceImage object
    	try {
	    	PhotoRequest pr	= new PhotoRequest(obj.getInt("id"),
	    			obj.getInt("lat"), obj.getInt("lon"),
	    			obj.getString("resource"), obj.getString("submitted_date"));
	    	ResourceImage ri	= new ResourceImage();
	    	ri.setPhotoRequest(pr);
//	    	try {
//	    		ri.setBitmapUri(getFullUri(obj.getString("resource")));
//	    	} catch (Exception e){
//	    		// Do nothing
//	    		Log.e("toResourceImage", e.toString());
//	    	}
	    	return ri;
    	} catch (JSONException e){
    		Log.e("toResourceImage", e.toString());
    		return null;
    	}

    }
    
	private JSONObject getContentObject(String method, HashMap<String, String> params)
	{
		String js = "";
		if (params == null)
			params	= new HashMap<String, String>();
		params.put("key", context.getString(R.string.api_key));		// Default param
				
		try
		{ 
			// Create a URLConnection object for a URL
		    URL url = new URL(createUrl(method, params));
		    URLConnection conn 		= url.openConnection();
		    InputStream response 	= new BufferedInputStream(conn.getInputStream());
		    BufferedReader reader 	= new BufferedReader(new InputStreamReader(response));
		    js	= reader.readLine();
		    Log.i("Web", js);
		}catch (Exception e) {
			Log.e("WebError", e.toString());
		}
				
		try {
			return new JSONObject(js);
		} catch (Exception e) {
			Log.e("Json", e.toString());
			return null;
		}
	}
	
	public String createUrl(String method, HashMap<String, String> params)
	{
		Iterator<String> keyIter = params.keySet().iterator();
		ArrayList<String> ps	= new ArrayList<String>();
		int i	= 0;
		while(keyIter.hasNext()) {
			String	key	= keyIter.next();	//(String)keyIter.next();
		    ps.add(key + "=" + params.get(key));
		}
		return String.format("%s/%s?%s", context.getString(R.string.base_uri),
							 method, join(ps, "&"));
	}    
    
	public static String join(Collection<String> s, String delimiter) {
	    StringBuffer buffer = new StringBuffer();
	    Iterator<String> iter = s.iterator();
	    while (iter.hasNext()) {
	        buffer.append(iter.next());
	        if (iter.hasNext()) {
	            buffer.append(delimiter);
	        }
	    }
	    return buffer.toString();
	}
}



