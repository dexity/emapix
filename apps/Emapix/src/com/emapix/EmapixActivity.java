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
	public class MarkerItemizedOverlay extends ItemizedOverlay<OverlayItem> {
		
		private OverlayItem mOverlay;
		Context mContext;

		public MarkerItemizedOverlay(Drawable defaultMarker) {
			//super(boundCenterBottom(defaultMarker));
			super(defaultMarker);
			//mContext = context;
			populate();	// Important
		}
		
		public void setOverlay(OverlayItem overlay) {
		    mOverlay = overlay;
		    populate();
		}	

		@Override
		protected boolean onTap(int index) {
			// No action
			return true;
		}	
		
		@Override
		protected OverlayItem createItem(int i) {
			return mOverlay;
		}
		
		@Override
		public int size() {
			if (mOverlay != null)
				return 1;
			return 0;
		}
	}	
	
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        EmapixMapView mView = (EmapixMapView) findViewById(R.id.mapview);
        mView.setBuiltInZoomControls(true);   
        
//        List<Overlay> mOverlays = mView.getOverlays();
//        Drawable drawable = this.getResources().getDrawable(R.drawable.androidmarker);
//        MarkerItemizedOverlay itemizedoverlay = new MarkerItemizedOverlay(drawable);        
//        mOverlays.add(itemizedoverlay);
        
        // Initial position
        GeoPoint point	= new GeoPoint(32818062,-117269440);
		MapController mController = mView.getController();
		mController.setZoom(14);
		mController.animateTo(point);
		
        mView.setOnLongpressListener(new EmapixMapView.OnLongpressListener() {
	        public void onLongpress(final MapView view, final GeoPoint lpPoint) {
	            runOnUiThread(new Runnable() {
		            public void run() {
		            	// Add image
		                List<Overlay> mOverlays = view.getOverlays();
		            	
		                Log.i("OVERLAYS", mOverlays.toString());
		                
		                Drawable drawable = view.getResources().getDrawable(R.drawable.androidmarker);
		                MarkerItemizedOverlay itemizedoverlay = new MarkerItemizedOverlay(drawable);//, view.getContext());        
		                
		            	OverlayItem overlayitem = new OverlayItem(lpPoint, "", "");
		            	itemizedoverlay.setOverlay(overlayitem);
		            	
		                mOverlays.add(itemizedoverlay);		            	
		            	
		                
//		            	List<Overlay> overlays = view.getOverlays();
//		            	// We added one overlay before
//		            	MarkerItemizedOverlay overlay	= (MarkerItemizedOverlay)overlays.get(0);
//		            	OverlayItem overlayitem = new OverlayItem(lpPoint, "", "");
//		            	overlay.setOverlay(overlayitem);
		            	
		                
//		                MapController mController = view.getController();
//		                mController.setZoom(14);
//		                mController.animateTo(lpPoint);
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

/*

	
	public class MarkerItemizedOverlay extends ItemizedOverlay {
		
		private ArrayList<OverlayItem> mOverlays = new ArrayList<OverlayItem>();
		Context mContext;

		public MarkerItemizedOverlay(Drawable defaultMarker) {
			//super(boundCenterBottom(defaultMarker));
			super(defaultMarker);
			//mContext = context;
		}
		
		public void setOverlay(OverlayItem overlay) {
			mOverlays.add(overlay);
		    populate();
		}	

		@Override
		protected boolean onTap(int index) {
			// No action
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
	
 */
