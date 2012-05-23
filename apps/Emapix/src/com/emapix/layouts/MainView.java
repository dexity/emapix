
package com.emapix.layouts;

import com.emapix.EmapixMapView;
import com.emapix.R;
import com.google.android.maps.GeoPoint;
import com.google.android.maps.MapActivity;
import com.google.android.maps.MapController;

import android.app.Activity;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

/*
 * I use here custom library which handles FragmentActivity and MapActivity issue.
 * 		https://github.com/petedoyle/android-support-v4-googlemaps
 * Caution needs to be taken for production!
 */

public class MainView extends FragmentActivity // MapActivity
{
	private SimpleMapView mView;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_map_view);
        mView = (SimpleMapView) findViewById(R.id.simplemapview);
        mView.setBuiltInZoomControls(true);   
        
        // Initial position
        GeoPoint point	= new GeoPoint(32818062,-117269440);
		MapController mController = mView.getController();
		mController.setZoom(14);
		mController.animateTo(point);
		
		// Attempt to use fragment
        ControlFragment details = new ControlFragment();
        details.setArguments(getIntent().getExtras());
        getSupportFragmentManager()
        	.beginTransaction()
        	.add(android.R.id.content, details)
        	//.setTransition( FragmentTransaction.TRANSIT_FRAGMENT_FADE )
        	.commit();
		
    }
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the currently selected menu XML resource.
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.controls, menu);        
                
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        
        return false;
    }
    
}
