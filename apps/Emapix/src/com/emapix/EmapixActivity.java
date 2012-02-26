package com.emapix;

import java.util.ArrayList;
import java.util.List;

import android.app.AlertDialog;
import android.content.Context;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.MeasureSpec;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageButton;
import android.widget.LinearLayout;

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
			populate();		// Important
		}
		
		public void addOverlay(OverlayItem overlay) {
			mOverlays.clear();	// Not very efficient
			mOverlays.add(overlay);
		    populate();
		}	
		
		public void removeOverlays() {
			mOverlays.clear();
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
        
        // Setting bubble
        LayoutInflater inflater = this.getLayoutInflater();
        LinearLayout bubble = (LinearLayout) inflater.inflate(R.layout.bubble, mView, false);

        /*
        //Set up the bubble's close button
        ImageButton bubbleClose = (ImageButton) bubble.findViewById(R.id.sendreq);
        bubbleClose.setOnClickListener(new View.OnClickListener() {
        	public void onClick(View v) {
        		//Animation fadeOut = AnimationUtils.loadAnimation(this, R.anim.fadeout);
        		//bubble.startAnimation(fadeOut);
        		//bubble.setVisibility(View.GONE);
        	}
        });        
        */
        
        
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
    
/*    
    private void displaySearchResultBubble(final SearchResult result) {
    	//Hide the bubble if it's already showing for another result
    	map.removeView(bubble);
    	bubble.setVisibility(View.GONE);

    	//Set some view content
    	TextView venueName = (TextView) bubble.findViewById(R.id.venuename);
    	venueName.setText(result.getName());

    	//This is the important bit - set up a LayoutParams object for positioning of the bubble.
    	//This will keep the bubble floating over the GeoPoint result.getPoint() as you move the MapView around,
    	//but you can also keep the view in the same place on the map using a different LayoutParams constructor
    	MapView.LayoutParams params = new MapView.LayoutParams(
    		LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT,
     		result.getPoint(), MapView.LayoutParams.BOTTOM_CENTER);

    	bubble.setLayoutParams(params);

    	map.addView(bubble);
    	//Measure the bubble so it can be placed on the map
    	map.measure(MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED), MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED));

    	//Runnable to fade the bubble in when we've finished animatingTo our OverlayItem (below)
    	Runnable r = new Runnable() {
    		public void run() {
    			Animation fadeIn = AnimationUtils.loadAnimation(activity, R.anim.fadein);
    			bubble.setVisibility(View.VISIBLE);
    			bubble.startAnimation(fadeIn);
    		}
    	};

    	//This projection and offset finds us a new GeoPoint slightly below the actual OverlayItem,
    	//which means the bubble will end up being centered nicely when we tap on an Item.
    	Projection projection = map.getProjection();
    	Point p = new Point();

    	projection.toPixels(result.getPoint(), p);
    	p.offset(0, -(bubble.getMeasuredHeight() / 2));
    	GeoPoint target = projection.fromPixels(p.x, p.y);

    	//Move the MapView to our point, and then call the Runnable that fades in the bubble.
    	mapController.animateTo(target, r);
     }    
*/
}

