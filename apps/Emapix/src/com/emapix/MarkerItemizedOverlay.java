
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
	Context mContext;
	MapView mView;

	public MarkerItemizedOverlay(Drawable defaultMarker, MapView mv) {
		super(boundCenterBottom(defaultMarker));
		//mContext = context;
		mView	= mv;
		setLastFocusedIndex(-1);
		populate();		// Important
	}
	
	public void addOverlay(OverlayItem overlay) {
		mOverlays.add(overlay);
	    populate();
	}	
	 
	public void removeOverlay(OverlayItem overlay) { //throws IndexOutOfBoundsException {
		//setLastFocusedIndex(-1);
		mOverlays.remove(overlay);
		populate();
	}	
	
	public void removeOverlays() {
		mOverlays.clear();
	}
	
	@Override
	protected boolean onTap(int index) {
		List<Overlay> mOverlays = mView.getOverlays();
		mOverlays.remove(this);		// Can throw an exception?
		return true;
	}	
	
//	public boolean onTap(GeoPoint p, MapView mapView) {
//		List<Overlay> mOverlays = mapView.getOverlays();
//		mOverlays.remove(this);
//		return true;
//	}

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