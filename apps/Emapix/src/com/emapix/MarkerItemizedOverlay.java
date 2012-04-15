
package com.emapix;

import java.util.ArrayList;

import android.content.Context;
import android.graphics.drawable.Drawable;

import com.google.android.maps.ItemizedOverlay;
import com.google.android.maps.OverlayItem;


// Move to a separate class?
public class MarkerItemizedOverlay extends ItemizedOverlay {
	
	private ArrayList<OverlayItem> mOverlays = new ArrayList<OverlayItem>();
	Context mContext;

	public MarkerItemizedOverlay(Drawable defaultMarker, Context context) {
		super(boundCenterBottom(defaultMarker));
		mContext = context;
		populate();		// Important
	}
	
	public void addOverlay(OverlayItem overlay) {
		mOverlays.clear();	// Not very efficient
		mOverlays.add(overlay);
	    populate();
	}	
	
	public void removeOverlays() {
		mOverlays.clear();
	}

	@Override
	protected boolean onTap(int index) {
		return true;
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
