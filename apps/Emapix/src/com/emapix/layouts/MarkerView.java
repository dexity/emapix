package com.emapix.layouts;

import android.os.Bundle;
import android.util.Log;

import com.google.android.maps.GeoPoint;

public class MarkerView extends MainView 
{
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Add bubble
        GeoPoint point	= new GeoPoint(32805727, -117246781);
		setupMarker(point);
    }
        
}