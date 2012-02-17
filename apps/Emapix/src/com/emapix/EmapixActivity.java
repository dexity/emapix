package com.emapix;

import android.app.Activity;
import android.os.Bundle;
import com.google.android.maps.MapView;
import com.google.android.maps.MapActivity;

public class EmapixActivity extends MapActivity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        MapView mapView = (MapView) findViewById(R.id.mapview);
        mapView.setBuiltInZoomControls(true);        
    }
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }   
    
}