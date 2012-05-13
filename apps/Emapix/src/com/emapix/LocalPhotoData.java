package com.emapix;

import android.content.Context;

import com.emapix.EmapixDB.PhotoRequestCursor;
import com.google.android.maps.GeoPoint;

class LocalPhotoData implements IPhotoData 
{
	private EmapixDB db;
	
	public LocalPhotoData(Context context) {
		db			= new EmapixDB(context);
	}
	
    public ResourceImage get(int res_id) {
    	PhotoRequestCursor c	= db.getPhotoRequests();
    	if (c.getCount() == 0)
    		return null;
    	c.moveToPosition(0);	// take the first record
    	ResourceImage ri = new ResourceImage();
		ri.setPhotoRequest(new PhotoRequest(c.getLat(), c.getLon(), 
				  c.getResId(), c.getResource(), c.getDate()));    	
    	return ri;
    }
    
    public ResourceImage[] getAll() {
    	PhotoRequestCursor c	= db.getPhotoRequests();    	
    	ResourceImage[] ri	= new ResourceImage[c.getCount()];
    	for (int i=0; i<c.getCount(); i++) {
    		c.moveToPosition(i);
    		ri[i]	= new ResourceImage();
    		ri[i].setPhotoRequest(new PhotoRequest(c.getLat(), c.getLon(), 
    							  c.getResId(), c.getResource(), c.getDate()));
    	}
    	return ri;
    }
    
    public boolean setResource(int res_id, String resource) {
    	db.updateMarker(res_id, resource);
    	return true;	// XXX: Fix
    }
    
    public ResourceImage add(int lat, int lon) {
    	// generate resource
    	long _id	= db.addRequest(lat, lon);	// returns _id
    	if (_id == -1)
    		return null;
    	String date	= String.format("%s", System.currentTimeMillis()/1000);
    	// Notes: 
    	//		- Use get(rid) instead. Requires separate call to db
    	// 		- For now _id == res_id
    	//		- Generate resource. For now it is null
    	int res_id	= (int)_id;	// Temp
    	db.updateResId(_id);	// Temp
    	
    	ResourceImage ri = new ResourceImage();
		ri.setPhotoRequest(new PhotoRequest(lat, lon, res_id, null, date));  
		return ri;
    }
    
    public boolean remove(int res_id) {
    	db.deleteRequest(res_id);
    	return true;	// XXX: Fix
    }
    
    public boolean isEmpty(int res_id) {
    	return get(res_id) == null;
    }
    
    public int size() {
    	// useful?
    	return 0;
    }
}