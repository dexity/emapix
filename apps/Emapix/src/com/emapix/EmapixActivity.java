package com.emapix;

import java.util.ArrayList;
import java.util.List;

import android.app.AlertDialog;
import android.content.Context;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;

import com.google.android.maps.GeoPoint;
import com.google.android.maps.ItemizedOverlay;
import com.google.android.maps.MapController;
import com.google.android.maps.MapView;
import com.google.android.maps.MapActivity;
import com.google.android.maps.Overlay;
import com.google.android.maps.OverlayItem;

public class EmapixActivity extends MapActivity {
	
	// Move to a separate class?
	public class MarkerItemizedOverlay extends ItemizedOverlay {
		
		private ArrayList<OverlayItem> mOverlays = new ArrayList<OverlayItem>();
		Context mContext;

		public MarkerItemizedOverlay(Drawable defaultMarker, Context context) {
			super(boundCenterBottom(defaultMarker));
			mContext = context;
			populate();	// Important
		}
		
		public void addOverlay(OverlayItem overlay) {
			mOverlays.clear();
			mOverlays.add(overlay);
		    populate();
		}	

		@Override
		protected boolean onTap(int index) {
			return true;
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
	
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        EmapixMapView mView = (EmapixMapView) findViewById(R.id.mapview);
        mView.setBuiltInZoomControls(true);   
        
        // Initial position
        GeoPoint point	= new GeoPoint(32818062,-117269440);
		MapController mController = mView.getController();
		mController.setZoom(14);
		mController.animateTo(point);

		List<Overlay> mOverlays = mView.getOverlays();
        Drawable drawable = this.getResources().getDrawable(R.drawable.androidmarker);
        MarkerItemizedOverlay itemizedoverlay = new MarkerItemizedOverlay(drawable, this);        
        mOverlays.add(itemizedoverlay);
        		
        mView.setOnLongpressListener(new EmapixMapView.OnLongpressListener() {
	        public void onLongpress(final MapView view, final GeoPoint lpPoint) {
	            runOnUiThread(new Runnable() {
		            public void run() {
		            	// Add image
	                
		            	List<Overlay> overlays = view.getOverlays();
		            	// We added one overlay before
		            	MarkerItemizedOverlay overlay	= (MarkerItemizedOverlay)overlays.get(0);
		            	OverlayItem overlayitem = new OverlayItem(lpPoint, "", "");
		            	overlay.addOverlay(overlayitem);

		            	view.invalidate();
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

