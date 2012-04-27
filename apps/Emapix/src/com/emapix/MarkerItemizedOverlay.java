
package com.emapix;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Vector;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.util.Log;

import com.google.android.maps.ItemizedOverlay;
import com.google.android.maps.MapView;
import com.google.android.maps.OverlayItem;

// XXX: Manage overlay items

public class MarkerItemizedOverlay extends ItemizedOverlay<OverlayItem> {
	
	//private ArrayList<OverlayItem> mOverlays = new ArrayList<OverlayItem>();
	//private Vector<OverlayItem> mOverlays = new Vector<OverlayItem>();	// change
	HashMap<Integer, OverlayItem> mOverlays = new HashMap<Integer, OverlayItem>();
	int overlayIndex = 0;
	Context mContext;

	public MarkerItemizedOverlay(Drawable defaultMarker, Context context) {
		super(boundCenterBottom(defaultMarker));
		mContext = context;
		setLastFocusedIndex(-1);
		populate();		// Important
	}
	
	public void addOverlay(OverlayItem overlay) {
		//mOverlays.add(overlay);
		//setLastFocusedIndex(-1);
		Log.i("OVERLAY", String.format("> %d", overlayIndex));
		mOverlays.put(overlayIndex, overlay);
		overlayIndex++;
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
		//setLastFocusedIndex(-1);
		Log.i("TAP", String.format("> %d", index));
		mOverlays.remove(index);
//		if (mOverlays.size() > index ) {
//			Log.i("TAP", "Not empty");
//			OverlayItem item = mOverlays.get(index);
//			//removeOverlay(item);
//			mOverlays.remove(index);
//			setLastFocusedIndex(-1);
//			populate();	
//			return true;
//		}
		return true;
	}	
	

	@Override
	protected OverlayItem createItem(int i) {
		Log.i("CREATE", String.format("%d", i));
		//setLastFocusedIndex(-1);
		return mOverlays.get(i);
//		try {
//		return mOverlays.get(i);
//		}
//		catch( Exception e) {
//			Log.i("CREATE", String.format("%s", e));
//			return null;
//		}
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