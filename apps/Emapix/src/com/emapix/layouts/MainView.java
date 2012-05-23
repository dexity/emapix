
package com.emapix.layouts;

import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.emapix.R;
import com.google.android.maps.GeoPoint;
import com.google.android.maps.MapController;
import com.google.android.maps.MapView;

import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuItem;

/*
 * I use here custom library which handles FragmentActivity and MapActivity issue.
 * 		https://github.com/petedoyle/android-support-v4-googlemaps
 * Caution needs to be taken for production!
 */

public class MainView extends SherlockFragmentActivity
{
	private NavigationFragment navFragment;
	private MapFragment mMapFragment;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_map_view);
        
        Exchanger.mMapView = new MapView(this, getString(R.string.map_api_key));
        Exchanger.mMapView.setBuiltInZoomControls(true);   
        
        // Initial position
        GeoPoint point	= new GeoPoint(32818062,-117269440);
		MapController mController = Exchanger.mMapView.getController();
		mController.setZoom(14);
		mController.animateTo(point);
		
		setupFragments();
    }
    
	private void setupFragments() {
		final FragmentTransaction ft = getSupportFragmentManager().beginTransaction();

		/*
		 * If the activity is killed while in BG, it's possible that the
		 * fragment still remains in the FragmentManager, so, we don't need to
		 * add it again.
		 */
		navFragment	= (NavigationFragment) getSupportFragmentManager().findFragmentByTag(NavigationFragment.TAG);
        if (navFragment == null) {
        	navFragment = new NavigationFragment();
        	ft.add(R.id.navigation, navFragment, NavigationFragment.TAG);
        }
        
		mMapFragment = (MapFragment) getSupportFragmentManager().findFragmentByTag(MapFragment.TAG);
        if (mMapFragment == null) {
        	mMapFragment = new MapFragment();
        	ft.add(R.id.fragment_container, mMapFragment, MapFragment.TAG);
        }
        
        ft.commit();
	}
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }
    
	public static class Exchanger {
		// We will use this MapView always.
    	public static MapView mMapView;
    }    
    
	
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the currently selected menu XML resource.
    	getSupportMenuInflater().inflate(R.menu.menu, menu);
		return true;
		
//        MenuInflater inflater = getMenuInflater();
//        inflater.inflate(R.menu.controls, menu);        
//                
//        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // XXX: Finish
    	return super.onOptionsItemSelected(item);
    }
    
}
