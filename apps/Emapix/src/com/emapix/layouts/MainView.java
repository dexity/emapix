
package com.emapix.layouts;

import java.util.ArrayList;
import java.util.List;

import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.emapix.R;
import com.google.android.maps.GeoPoint;
import com.google.android.maps.ItemizedOverlay;
import com.google.android.maps.MapController;
import com.google.android.maps.MapView;
import com.google.android.maps.Overlay;
import com.google.android.maps.OverlayItem;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.BitmapFactory.Options;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.ViewGroup.LayoutParams;
import android.widget.LinearLayout;

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
	protected Drawable marker;
	protected List<Overlay> mOverlays;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_map_view);
        
        Exchanger.mMapView = new MapView(this, getString(R.string.map_api_key));
        Exchanger.mMapView.setBuiltInZoomControls(true);   
                
        // Initial position
        GeoPoint point	= new GeoPoint(32855636, -117270762);	// (32818062,-117269440)
        
		MapController mController = Exchanger.mMapView.getController();
		mController.setZoom(14);
		mController.animateTo(point);
		
		setupFragments();
    }
    
    protected Drawable createMarker(int res_id, Options opts) {
		Bitmap bm = BitmapFactory.decodeResource(getResources(), res_id, opts);
		if (bm != null) {
			return new BitmapDrawable(getResources(), bm);
		}
		
    	return null;
    }    
    
    protected void setupMarker(GeoPoint point) {
		Options opts = new BitmapFactory.Options();
		opts.inDensity = 400;
    	
        marker	= createMarker(R.drawable.redmarker, opts);
        mOverlays	= Exchanger.mMapView.getOverlays();
        MarkerOverlay mo	= new MarkerOverlay(marker, point);
        mo.addOverlay(new OverlayItem(point, null, null));
        mOverlays.add(mo);
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
    
	protected class MarkerOverlay extends ItemizedOverlay<OverlayItem> {
		// Minimal version for overlay
		private ArrayList<OverlayItem> mmOverlays = new ArrayList<OverlayItem>();
		
		public MarkerOverlay(Drawable defaultMarker, GeoPoint point) {
			super(boundCenterBottom(defaultMarker));
			
			populate();
		}
		public void addOverlay(OverlayItem overlay) {
			mmOverlays.add(overlay);
		    populate();
		}			
		@Override
		protected OverlayItem createItem(int i) {
			return mmOverlays.get(i);
		}		
		@Override
		public int size() {
			return mmOverlays.size();
		}		
	}
	
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the currently selected menu XML resource.
    	getSupportMenuInflater().inflate(R.menu.menu, menu);
		return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // XXX: Finish
    	return super.onOptionsItemSelected(item);
    }
    
    // Not quite related to the view
    protected LinearLayout bubbleFactory(int resource, GeoPoint point) {
        LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        LinearLayout layout = (LinearLayout) inflater.inflate(resource, Exchanger.mMapView, false);

    	MapView.LayoutParams params = new MapView.LayoutParams(
		                		450, LayoutParams.WRAP_CONTENT,
		                 		point, MapView.LayoutParams.BOTTOM_CENTER);
    	params.mode = MapView.LayoutParams.MODE_MAP;
    	layout.setLayoutParams(params);    	
        return layout;
    }
    
    
}
