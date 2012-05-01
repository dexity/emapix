
package com.emapix;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import android.app.AlertDialog;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.BitmapFactory.Options;
import android.graphics.Point;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.ScaleDrawable;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.MeasureSpec;
import android.view.ViewGroup.LayoutParams;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.emapix.EmapixDB.PhotoRequestCursor;
import com.google.android.maps.GeoPoint;
import com.google.android.maps.ItemizedOverlay;
import com.google.android.maps.MapController;
import com.google.android.maps.MapView;
import com.google.android.maps.MapActivity;
import com.google.android.maps.Overlay;
import com.google.android.maps.OverlayItem;
import com.google.android.maps.Projection;
import android.graphics.drawable.BitmapDrawable;



public class EmapixActivity extends MapActivity {
	
	private LinearLayout bubble;
	private EmapixMapView mView;
	private EmapixDB db;
	private MarkerItemizedOverlay cOverlay;
	private MarkerItemizedOverlay itemOverlay;
	List<Overlay> mOverlays;
	Drawable drawable;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        mView = (EmapixMapView) findViewById(R.id.mapview);
        mView.setBuiltInZoomControls(true);   
        
        // Initial position
        GeoPoint point	= new GeoPoint(32818062,-117269440);
		MapController mController = mView.getController();
		mController.setZoom(14);
		mController.animateTo(point);

    	//drawable = getResources().getDrawable(R.drawable.redmarker);
		Options opts = new BitmapFactory.Options();
		opts.inDensity = 400;

		Bitmap bm = BitmapFactory.decodeResource(getResources(), R.drawable.redmarker, opts);
		if (bm != null) {
			drawable = new BitmapDrawable(getResources(), bm);
		}
		
    	mOverlays = mView.getOverlays();

    	populateMarkers(drawable);
    	
//		List<Overlay> mOverlays = mView.getOverlays();
//        Drawable drawable = this.getResources().getDrawable(R.drawable.androidmarker);
//        MarkerItemizedOverlay itemizedoverlay = new MarkerItemizedOverlay(drawable, this);        
//        mOverlays.add(itemizedoverlay);
        
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
		            	showRequestBubble(lpPoint);		   
		            }
		        });
	        }
        });
		
    }
    
    // Bubbles    
    public void showRequestBubble(final GeoPoint point) {
        // Sets request bubble
        LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        bubble = (LinearLayout) inflater.inflate(R.layout.bubble, mView, false);
        
        // Remove bubble  
        if (mView.findViewById(bubble.getId()) != null ) {
        	mView.removeViewAt(0);				// XXX: Hardcoded.
        	bubble.setVisibility(View.GONE);
        }

    	EmapixMapView.LayoutParams params = new EmapixMapView.LayoutParams(
		                		370, LayoutParams.WRAP_CONTENT,
		                 		point, EmapixMapView.LayoutParams.BOTTOM_CENTER);
    	params.mode = MapView.LayoutParams.MODE_MAP;
        bubble.setLayoutParams(params);
    	// Set text
    	TextView tv = (TextView)bubble.findViewById(R.id.locationname);
    	tv.setText(String.format("Location: %f; %f", point.getLatitudeE6()*1E-6, point.getLongitudeE6()*1E-6));
        // Set close button
    	ImageView btn_close	= (ImageView) bubble.findViewById(R.id.bubble_close);
        btn_close.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	bubble.setVisibility(View.GONE);
            }
        });
        // Set send button
        Button btn_send	= (Button) bubble.findViewById(R.id.sendreq);
        btn_send.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	sendRequest(point);
            }
        });
        
        if (mView.findViewById(bubble.getId()) == null)
        	mView.addView(bubble);
    	mView.measure(MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED), 
    				 MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED));
    	
    	bubble.setVisibility(View.VISIBLE);   	
    }
    
    
    public void showActionBubble(MarkerItemizedOverlay currOverlay, final GeoPoint point) {
    	
    	// Hide current overlay
    	cOverlay = currOverlay;
    	mOverlays.remove(cOverlay);
	
    	//cOverlay.getOverlayItems().get(0).setMarker(null);
    	
        // Sets request bubble
        LayoutInflater inflater = (LayoutInflater) EmapixActivity.this
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        bubble = (LinearLayout) inflater.inflate(R.layout.action_bubble, mView, false);
        
        // Remove bubble  
        if (mView.findViewById(bubble.getId()) != null ) {
        	mView.removeViewAt(0);				// XXX: Hardcoded.
        	bubble.setVisibility(View.GONE);
        }

    	EmapixMapView.LayoutParams params = new EmapixMapView.LayoutParams(
		                		370, LayoutParams.WRAP_CONTENT,
		                 		point, EmapixMapView.LayoutParams.BOTTOM_CENTER);
    	params.mode = MapView.LayoutParams.MODE_MAP;
        bubble.setLayoutParams(params);
    	// Set text
    	TextView tv = (TextView)bubble.findViewById(R.id.locationname);
    	tv.setText(String.format("Location: %f; %f", point.getLatitudeE6()*1E-6, point.getLongitudeE6()*1E-6));
        
    	// Set close button
    	ImageView btn_close	= (ImageView) bubble.findViewById(R.id.bubble_close);
        btn_close.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// Return to current marker
            	mOverlays.add(cOverlay);
            	bubble.setVisibility(View.GONE);
            }
        });
        
        // Set take picture button
        Button btn_take	= (Button) bubble.findViewById(R.id.take_pic);
        btn_take.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// XXX: Takes picture
            	
            }
        });
        
        // Set remove marker button
        Button btn_remove	= (Button) bubble.findViewById(R.id.remove_marker);
        btn_remove.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// Remove marker
            	cOverlay.removeOverlay();
            	bubble.setVisibility(View.GONE);
            }
        });
        
        if (mView.findViewById(bubble.getId()) == null) {
        	mView.addView(bubble);
        }
    	mView.measure(MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED), 
    				 MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED));
    	
    	bubble.setVisibility(View.VISIBLE);   	
    }
    
    
    
    
    private void populateMarkers(Drawable drawable) {
    	// Populates markers from database    	
    	db	= new EmapixDB(this);
    	PhotoRequestCursor cursor	= db.getPhotoRequests();
    	for (int i=0; i<cursor.getCount(); i++) {
    		cursor.moveToPosition(i);
    		GeoPoint point = new GeoPoint((int) cursor.getLat(), (int) cursor.getLon());
    		showMarker(point, cursor.getId());
    	}
    }
    
    private void sendRequest(GeoPoint point)
    {
    	// Close bubble
    	bubble.setVisibility(View.GONE);    	
    	addMarker(point);
    }
    
    public EmapixDB getEmapixDB() {
    	return db;
    }
    
    public EmapixMapView getMapView() {
    	return mView;
    }
    
    public void addMarker(GeoPoint point) {
    	// Add DB record
    	long id = db.addRequest(point.getLatitudeE6(), point.getLongitudeE6());
    	showMarker(point, id);
    }
    
    public void showMarker(GeoPoint point, long id) {
    	// Show red marker
    	OverlayItem item	= new OverlayItem(point, null, null);   
    	itemOverlay	= new MarkerItemizedOverlay(drawable, this, point, id); //.getContext());
    	itemOverlay.addOverlay(item);
    	mOverlays.add(itemOverlay);
    }
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }  
       
}
    

//    private void displayBubble(MapView map, GeoPoint point) {
//    	
//        // Setting bubble
//        LayoutInflater inflater = this.getLayoutInflater();
//        LinearLayout bubble = (LinearLayout) inflater.inflate(R.layout.bubble, map, false);
//    	
//        //Set up the bubble's send button
//        Button btnSend = (Button) bubble.findViewById(R.id.sendreq);
//        btnSend.setOnClickListener(new View.OnClickListener() {
//        	public void onClick(View v) {
//        		// Send request
//        		//Animation fadeOut = AnimationUtils.loadAnimation(this, R.anim.fadeout);
//        		//bubble.startAnimation(fadeOut);
//        		//bubble.setVisibility(View.GONE);
//        	}
//        });              
//        
//    	//Hide the bubble if it's already showing for another result
//    	map.removeView(bubble);
//    	bubble.setVisibility(View.GONE);
//
//    	//Set some view content
//    	TextView venueName = (TextView) bubble.findViewById(R.id.locationname);
//    	venueName.setText("Location");//point.toString());
//    	private void displayBubble(MapView map, GeoPoint point) {
//        	
//            // Setting bubble
//            LayoutInflater inflater = this.getLayoutInflater();
//            LinearLayout bubble = (LinearLayout) inflater.inflate(R.layout.bubble, map, false);
//        	
//            //Set up the bubble's send button
//            Button btnSend = (Button) bubble.findViewById(R.id.sendreq);
//            btnSend.setOnClickListener(new View.OnClickListener() {
//            	public void onClick(View v) {
//            		// Send request
//            		//Animation fadeOut = AnimationUtils.loadAnimation(this, R.anim.fadeout);
//            		//bubble.startAnimation(fadeOut);
//            		//bubble.setVisibility(View.GONE);
//            	}
//            });              
//            
//        	//Hide the bubble if it's already showing for another result
//        	map.removeView(bubble);
//        	bubble.setVisibility(View.GONE);
//
//        	//Set some view content
//        	TextView venueName = (TextView) bubble.findViewById(R.id.locationname);
//        	venueName.setText("Location");//point.toString());
//
//        	//This is the important bit - set up a LayoutParams object for positioning of the bubble.
//        	//This will keep the bubble floating over the GeoPoint result.getPoint() as you move the MapView around,
//        	//but you can also keep t
//    	//This is the important bit - set up a LayoutParams object for positioning of the bubble.
//    	//This will keep the bubble floating over the GeoPoint result.getPoint() as you move the MapView around,
//    	//but you can also keep the view in the same place on the map using a different LayoutParams constructor
//    	EmapixMapView.LayoutParams params = new EmapixMapView.LayoutParams(
//    		LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT,
//     		point, EmapixMapView.LayoutParams.BOTTOM_CENTER);
//
//    	bubble.setLayoutParams(params);
//
//    	map.addView(bubble);
//    	//Measure the bubble so it can be placed on the map
//    	map.measure(MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED), MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED));
//
//    	//Runnable to fade the bubble in when we've finished animatingTo our OverlayItem (below)
//    	Runnable r = new Runnable() {
//    		public void run() {    			
//    			//Animation fadeIn = AnimationUtils.loadAnimation(EmapixActivity.this, R.anim.fadein);
//    			// ???
//    			EmapixMapView mView = (EmapixMapView) findViewById(R.id.mapview);
//    	        LayoutInflater inflater = EmapixActivity.this.getLayoutInflater();
//    	        LinearLayout bubble = (LinearLayout) inflater.inflate(R.layout.bubble, mView, false);    			
//
//    	        bubble.setVisibility(View.VISIBLE);
//    	        mView.invalidate();
//    			//bubble.startAnimation(fadeIn);
//    		}
//    	};
//
//    	//This projection and offset finds us a new GeoPoint slightly below the actual OverlayItem,
//    	//which means the bubble will end up being centered nicely when we tap on an Item.
//    	Projection projection = map.getProjection();
//    	Point p = new Point();
//
//    	projection.toPixels(point, p);
//    	p.offset(0, -(bubble.getMeasuredHeight() / 2));
//    	GeoPoint target = projection.fromPixels(p.x, p.y);
//
//    	//Move the MapView to our point, and then call the Runnable that fades in the bubble.
//    	MapController mController = map.getController();
//    	mController.animateTo(target, r);
//    	//bubble.setVisibility(View.VISIBLE);
//     }    
    
//}

