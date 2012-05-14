
package com.emapix;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import android.util.Log;

import com.google.android.maps.GeoPoint;
import com.google.android.maps.ItemizedOverlay;
import com.google.android.maps.MapView;
import com.google.android.maps.Overlay;
import com.google.android.maps.OverlayItem;

// Note: Context is not stored in MarkerOverlay.

// XXX: Refactor MarkerOverlay

public class MarkerOverlay extends ItemizedOverlay<OverlayItem> {

	private GeoPoint point;
	private Drawable marker;	// marker image
	private ResourceImage rImage;	// XXX 
	private String resource;	// XXX: Remove; 
	private Bitmap image;		// XXX: Remove; image related to image
	private long id;			// XXX: Remove; db record id
	
	private ArrayList<OverlayItem> mOverlays = new ArrayList<OverlayItem>(); // Holds one item only!
	private MapView mView;
	private EmapixActivity activity;

	public MarkerOverlay(Drawable defaultMarker, EmapixActivity activity, 
						 GeoPoint point, long id, String resource) {
		super(boundCenterBottom(defaultMarker));
		marker	= defaultMarker;
		mView	= activity.getMapView();
		this.activity 	= activity;
		this.point		= point;
		this.id 		= id;
		this.resource	= resource;
		populate();		// Important
	}
	
	public void setImage(Bitmap image) {
		this.image = image;
	}
	
	public Bitmap getImage() {
		return image;
	}
	
	public void addOverlay(OverlayItem overlay) {
		mOverlays.add(overlay);
	    populate();
	}	
	 
	public void removeOverlay(OverlayItem overlay) {
		mOverlays.remove(overlay);
		populate();
	}	
	
	public void removeOverlays() {
		mOverlays.clear();
	}
	
	@Override
	protected boolean onTap(int index) {
		if (image != null)
			activity.showViewBubble(this);
		else
			activity.showActionBubble(this);
		
		return true;
	}	
	
	// Move to activity?
	public void removeOverlay() {
		List<Overlay> mOverlays = mView.getOverlays();
		mOverlays.remove(this);		// Can throw an exception?

		IPhotoData pd	= activity.getPhotoData();
		pd.remove((int)id);
	}
	
	public long getId() {
		return id;
	}
	
	GeoPoint getPoint() {
		return point;
	}
	
	String getResource() {
		return resource;
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

