package com.emapix.layouts;

import android.content.Context;
import android.os.Bundle;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.actionbarsherlock.app.SherlockFragment;
import com.emapix.layouts.MainView.Exchanger;

public class MapFragment extends SherlockFragment {

	public static final String TAG = "mapFragment";
	
	public MapFragment() {}
	
	@Override
	public void onCreate(Bundle arg0) {
		super.onCreate(arg0);
		setRetainInstance(true);
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup vg, Bundle data) {
		// The Activity created the MapView for us, so we can do some init stuff.
		Exchanger.mMapView.setClickable(true);
		Exchanger.mMapView.setBuiltInZoomControls(true); // If you want.

		/*
		 * If you're getting Exceptions saying that the MapView already has
		 * a parent, uncomment the next lines of code, but I think that it
		 * won't be necessary. In other cases it was, but in this case I
		 * don't this should happen.
		 */
		/*
		 * final ViewGroup parent = (ViewGroup) Exchanger.mMapView.getParent();
		 * if (parent != null) parent.removeView(Exchanger.mMapView);
		 */
		
		return Exchanger.mMapView;
	}
}
