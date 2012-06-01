package com.emapix.layouts;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import com.actionbarsherlock.app.SherlockFragment;
import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.emapix.R;
import com.emapix.layouts.MainView.Exchanger;
import com.google.android.maps.GeoPoint;
import com.google.android.maps.MapController;
import com.google.android.maps.MapView;

public class PhotoView extends SherlockFragmentActivity
{
	private NavigationFragment navFragment;
	private PhotoViewFragment photoFragment;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_map_view);
        
		// Code duplication (MainView)
        Exchanger.mMapView = new MapView(this, getString(R.string.map_api_key));
        Exchanger.mMapView.setClickable(true);
        Exchanger.mMapView.setBuiltInZoomControls(true);
        // Initial position
        GeoPoint point	= new GeoPoint(32818062,-117269440);            
		MapController mController = Exchanger.mMapView.getController();
		mController.setZoom(14);
		mController.animateTo(point);        
        
        setupFragments();
    }
    
	private void setupFragments() {
		final FragmentTransaction ft = getSupportFragmentManager()
									   .beginTransaction();

		navFragment	= (NavigationFragment) getSupportFragmentManager().findFragmentByTag(NavigationFragment.TAG);
        if (navFragment == null) {
        	navFragment = new NavigationFragment();
        	ft.add(R.id.navigation, navFragment, NavigationFragment.TAG);
        }
        
        photoFragment = (PhotoViewFragment) getSupportFragmentManager().findFragmentByTag(PhotoViewFragment.TAG);
        if (photoFragment == null) {
        	photoFragment = new PhotoViewFragment(this);
        	ft.add(R.id.fragment_container, photoFragment, PhotoViewFragment.TAG);
        }
        ft.commit();
	}   
	
    public class PhotoViewFragment extends SherlockFragment
    {
    	public static final String TAG = "photoViewFragment";	
    	private Context mContext;
    	 
    	public PhotoViewFragment(Context context){mContext = context;}
    	
    	@Override
    	public View onCreateView(LayoutInflater inflater, ViewGroup vg, Bundle data) {
    		// Take from db
    		GeoPoint point	= new GeoPoint(32818062,-117269440);   
    		
    		ScrollView sv	= (ScrollView)inflater.inflate(R.layout.test_photo_view, vg, false);    		
    		((FrameLayout)sv.findViewById(R.id.map_view)).addView(Exchanger.mMapView);
    		((TextView)sv.findViewById(R.id.description)).setText("Planning to hike in this place ...");
    		((TextView)sv.findViewById(R.id.locationname)).setText(String.format("Location:  %f; %f", point.getLatitudeE6()*1E-6, point.getLongitudeE6()*1E-6));
    		((TextView)sv.findViewById(R.id.request_username)).setText("dexity");
    		((TextView)sv.findViewById(R.id.request_time)).setText("May 18 2012, 5:13pm");
    		((TextView)sv.findViewById(R.id.submit_username)).setText("lunatix");
    		((TextView)sv.findViewById(R.id.submit_time)).setText("May 31 2012, 4:13pm");
    		return sv;
    	}
    }
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }    
}