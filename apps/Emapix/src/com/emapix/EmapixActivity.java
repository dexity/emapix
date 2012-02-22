package com.emapix;

import android.os.Bundle;

import com.google.android.maps.GeoPoint;
import com.google.android.maps.MapController;
import com.google.android.maps.MapView;
import com.google.android.maps.MapActivity;

public class EmapixActivity extends MapActivity {
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        EmapixMapView mView = (EmapixMapView) findViewById(R.id.mapview);
        mView.setBuiltInZoomControls(true);   
        
        GeoPoint point	= new GeoPoint(32818062,-117269440);
		MapController mController = mView.getController();
		mController.setZoom(14);
		mController.animateTo(point);
		
        mView.setOnLongpressListener(new EmapixMapView.OnLongpressListener() {
	        public void onLongpress(final MapView view, final GeoPoint longpressLocation) {
	            runOnUiThread(new Runnable() {
		            public void run() {
		                MapController mController = view.getController();
		                mController.setZoom(14);
		                mController.animateTo(longpressLocation);
		            }
		        });
	        }
        });

    }
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }   
    
}