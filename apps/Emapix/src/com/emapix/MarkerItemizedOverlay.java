
package com.emapix;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.util.Log;

import com.google.android.maps.GeoPoint;
import com.google.android.maps.ItemizedOverlay;
import com.google.android.maps.MapView;
import com.google.android.maps.Overlay;
import com.google.android.maps.OverlayItem;

// XXX: Manage overlay items

public class MarkerItemizedOverlay extends ItemizedOverlay<OverlayItem> {
	
	private ArrayList<OverlayItem> mOverlays = new ArrayList<OverlayItem>();
	Context mContext;	// ?
	GeoPoint point;
	MapView mView;
	Drawable marker;
	private String color;
	EmapixActivity activity;
	private long id;

	public MarkerItemizedOverlay(Drawable defaultMarker, EmapixActivity activity, String color, GeoPoint point, long id) {
		super(boundCenterBottom(defaultMarker));
		//mContext = context;
		marker	= defaultMarker;
		mView	= activity.getMapView();
		this.color		= color;
		this.activity 	= activity;
		this.point		= point;
		this.id 		= id;
		populate();		// Important
	}
	
	public void setColor(String color){
		this.color	= color;
	}
	
	public void addOverlay(OverlayItem overlay) {
		mOverlays.add(overlay);
	    populate();
	}	
	 
	public void removeOverlay(OverlayItem overlay) { //throws IndexOutOfBoundsException {
		mOverlays.remove(overlay);
		populate();
	}	
	
	public void removeOverlays() {
		mOverlays.clear();
	}
	
	@Override
	protected boolean onTap(int index) {
		if (color == "blue")
			activity.showViewBubble(this, point);
		else
			activity.showActionBubble(this, point);
		
		return true;
	}	
	
	// Move to activity?
	public void removeOverlay() {
		List<Overlay> mOverlays = mView.getOverlays();
		mOverlays.remove(this);		// Can throw an exception?
		EmapixDB db	= activity.getEmapixDB();
		db.deleteRequest(id);
	}
	
	public long getId() {
		return id;
	}
	
	public ArrayList<OverlayItem> getOverlayItems() {
		return mOverlays;
	}
	
	@Override
	protected OverlayItem createItem(int i) {
		return mOverlays.get(i);
	}

	@Override
	public int size() {
		return mOverlays.size();
	}
}		

//try {
//} catch(IndexOutOfBoundsException e1){
//      //throw e1;
//}