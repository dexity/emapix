package com.emapix;

import android.content.Context;

import com.emapix.EmapixDB.PhotoRequestCursor;
import com.google.android.maps.GeoPoint;

class LocalPhotoData implements IPhotoData 
{
	private EmapixDB db;
	private final Context mContext;
	
	public LocalPhotoData(Context context) {
		mContext	= context;
		db			= new EmapixDB(context);
	}
	
    public ResourceImage get(int res_id) {
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
    
    public void setResource(int res_id, String resource) {
    	
    }
    
    public void remove(int res_id) {
    	
    }
    
    public boolean isEmpty(int res_id) {
    	
    	return true;
    }
    
    public int size() {
    	
    	return 0;
    }
}