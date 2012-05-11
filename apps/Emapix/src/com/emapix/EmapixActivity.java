
package com.emapix;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.ByteArrayBody;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.DefaultHttpClient;

import android.app.AlertDialog;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.database.SQLException;
import android.graphics.Bitmap;
import android.graphics.Bitmap.CompressFormat;
import android.graphics.BitmapFactory;
import android.graphics.BitmapFactory.Options;
import android.graphics.Point;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.ScaleDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
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

// XXX: Cannot load more than 4 large pictures. Resources are not released 

public class EmapixActivity extends MapActivity {
	
	private LinearLayout bubble;
	private EmapixMapView mView;
	private EmapixDB db;	// remove
	private IPhotoData photoData;
	private MarkerOverlay cOverlay;
	private MarkerOverlay itemOverlay;
	List<Overlay> mOverlays;
	HashMap<String, Drawable> markers;
	Bitmap currImage;	// TEMP
	String currName;
	Uri currUri;
	
	private static final int PICK_IMAGE_CODE = 100;
	
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
		
		photoData	= new LocalPhotoData(this);
		
    	mOverlays = mView.getOverlays();
    	createMarkers();
    	populateMarkers();
        
    	// Set long press listener
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
    
    private void createMarkers() {
		Options opts = new BitmapFactory.Options();
		opts.inDensity = 400;

		markers	= new HashMap<String, Drawable>();
		markers.put("red", createMarker(R.drawable.redmarker, opts));
		markers.put("blue", createMarker(R.drawable.bluemarker, opts));
    }
    
    private Drawable createMarker(int res_id, Options opts) {
		Bitmap bm = BitmapFactory.decodeResource(getResources(), res_id, opts);
		if (bm != null) {
			return new BitmapDrawable(getResources(), bm);
		}
    	return null;
    }
    
    // Bubbles
    public void showRequestBubble(final GeoPoint point) {
        // Sets request bubble
    	cleanupBubbles(); 
    	
        LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        bubble = (LinearLayout) inflater.inflate(R.layout.bubble, mView, false);

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
    
    //private void setCloseButton(LinearLayout layout) {
    //	
    //}
    
    public void hideCurrOverlay(MarkerOverlay currOverlay) {
    	// Hide current overlay
    	cOverlay = currOverlay;
    	
    	mOverlays.remove(currOverlay);	
    }
    
    public void showCurrOverlay() {
    	mOverlays.add(cOverlay);	
    }
    
    public void cleanupBubbles() {
        // Removes bubble  
    	mView.removeAllViews();
    	
    	if (bubble != null)
    		bubble.setVisibility(View.GONE);
    }
    
    public void showActionBubble(MarkerOverlay currOverlay) {

    	GeoPoint point = currOverlay.getPoint();
        cleanupBubbles();    	
    	hideCurrOverlay(currOverlay);
    	
        // Sets request bubble
        LayoutInflater inflater = (LayoutInflater) EmapixActivity.this
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        bubble = (LinearLayout) inflater.inflate(R.layout.action_bubble, mView, false);
        
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
            	showCurrOverlay();
            	bubble.setVisibility(View.GONE);
            }
        });
        
        // Set take picture button
        Button btn_take	= (Button) bubble.findViewById(R.id.take_pic);
        btn_take.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {                
                // XXX: Takes picture
            	// Show preview bubble 
            	//showPreviewBubble(cOverlay);
            	
            	showCurrOverlay();
            	bubble.setVisibility(View.GONE);            	
            }
        });
        btn_take.setClickable(false); // XXX: Disables take picture button
        
        // Set select picture button
        Button btn_select	= (Button) bubble.findViewById(R.id.select_pic);
        btn_select.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// Select picture
            	Intent pickIntent = new Intent(Intent.ACTION_PICK);
            	pickIntent.setType("image/*");
            	startActivityForResult(pickIntent, PICK_IMAGE_CODE);
            	
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
    
    
    private void submitImage(Bitmap bm) {
    	// A VERY dirty way of submitting the image to S3

    	// XXX: Check if bitmap is JPEG or PNG
    	String uri = R.string.base_uri + "?key=" + R.string.api_key;
    	
    	try {
			ByteArrayOutputStream bos = new ByteArrayOutputStream();
			bm.compress(CompressFormat.JPEG, 75, bos);	// Fix compression format
			byte[] data = bos.toByteArray();
			// Http client
			HttpClient httpClient = new DefaultHttpClient();
			HttpPost postRequest = new HttpPost(uri);
			ByteArrayBody bab = new ByteArrayBody(data, currName);	// XXX: Fix filename

			MultipartEntity reqEntity = new MultipartEntity(
					HttpMultipartMode.BROWSER_COMPATIBLE);
			reqEntity.addPart("uploaded", bab);
			postRequest.setEntity(reqEntity);
			HttpResponse response = httpClient.execute(postRequest);
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					response.getEntity().getContent(), "UTF-8"));
			String sResponse;
			StringBuilder s = new StringBuilder();

			while ((sResponse = reader.readLine()) != null) {
				s = s.append(sResponse);
			}
			Log.i("SUBMIT", "Response: " + s);
		} catch (Exception e) {
			// handle exception here
			Log.e(e.getClass().getName(), e.getMessage());
		}    	
    	
    }
    
    
    public void showPreviewBubble(MarkerOverlay currOverlay) {
    	
    	GeoPoint point = currOverlay.getPoint();
    	cleanupBubbles();

        // Sets request bubble
        LayoutInflater inflater = (LayoutInflater) EmapixActivity.this
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        bubble = (LinearLayout) inflater.inflate(R.layout.preview_bubble, mView, false);
        
    	EmapixMapView.LayoutParams params = new EmapixMapView.LayoutParams(
		                		370, LayoutParams.WRAP_CONTENT,
		                 		point, EmapixMapView.LayoutParams.BOTTOM_CENTER);
    	params.mode = MapView.LayoutParams.MODE_MAP;
        bubble.setLayoutParams(params);

    	// Set close button
    	ImageView btn_close	= (ImageView) bubble.findViewById(R.id.bubble_close);
        btn_close.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// Return to current marker
            	showCurrOverlay();
            	bubble.setVisibility(View.GONE);
            }
        });
        
        // Set image view
        if (currImage != null) {
			ImageView image = (ImageView) bubble.findViewById(R.id.bubble_image);
			image.setImageBitmap(currImage);        	
        }        
        
        // Set submit button
        Button btn_submit	= (Button) bubble.findViewById(R.id.submit_pic);
        btn_submit.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// XXX: Submitting pic to server
            	
            	// Show blue marker            	
            	showMarker(cOverlay.getPoint(), cOverlay.getId(), currUri);
            	updateMarker(cOverlay.getId(), currUri);
            	cOverlay.setImage(currImage);
            	
            	bubble.setVisibility(View.GONE);
            	
            	// Submit to S3
            	submitImage(currImage);
            }
        });
        
        // Set take picture button
        Button btn_take	= (Button) bubble.findViewById(R.id.take_pic);
        btn_take.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// XXX: Takes picture
            	// Show preview bubble 
            	
            	
            }
        });
        btn_take.setClickable(false); // XXX: Disables take picture button
        
        // Set select button
        Button btn_select	= (Button) bubble.findViewById(R.id.select_pic);
        btn_select.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// Remove marker

            }
        });
        
        if (mView.findViewById(bubble.getId()) == null) {
        	mView.addView(bubble);
        }
    	mView.measure(MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED), 
    				 MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED));
    	
    	bubble.setVisibility(View.VISIBLE);   	
    }    
    
    public void showViewBubble(MarkerOverlay currOverlay) {
        // Sets request bubble
    	GeoPoint point = currOverlay.getPoint();
    	cleanupBubbles(); 
    	hideCurrOverlay(currOverlay);
    	
        LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        bubble = (LinearLayout) inflater.inflate(R.layout.view_bubble, mView, false);

    	EmapixMapView.LayoutParams params = new EmapixMapView.LayoutParams(
		                		370, LayoutParams.WRAP_CONTENT,
		                 		point, EmapixMapView.LayoutParams.BOTTOM_CENTER);
    	params.mode = MapView.LayoutParams.MODE_MAP;
        bubble.setLayoutParams(params);
        // Set close button
    	ImageView btn_close	= (ImageView) bubble.findViewById(R.id.bubble_close);
        btn_close.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	showCurrOverlay();
            	bubble.setVisibility(View.GONE);
            }
        });
        
        // Set image view
        if (currOverlay.getImage() != null) {
			ImageView image = (ImageView) bubble.findViewById(R.id.bubble_image);
			image.setImageBitmap(currOverlay.getImage());        	
        }        
        
        // Set remove button
        Button btn_send	= (Button) bubble.findViewById(R.id.remove_pic);
        btn_send.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// Remove marker and picture
            	
            	updateMarker(cOverlay.getId(), null);
            	showMarker(cOverlay.getPoint(), cOverlay.getId(), null);
            	bubble.setVisibility(View.GONE);            	
            }
        });
        
        if (mView.findViewById(bubble.getId()) == null)
        	mView.addView(bubble);
    	mView.measure(MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED), 
    				 MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED));
    	
    	bubble.setVisibility(View.VISIBLE);   	
    }
    
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent imageReturnedIntent) { 
        super.onActivityResult(requestCode, resultCode, imageReturnedIntent); 

        switch(requestCode) { 
        case PICK_IMAGE_CODE:
            if(resultCode == RESULT_OK){  
                Uri selectedImage = imageReturnedIntent.getData();
                currImage 	= getImageFromUri(selectedImage);
                currUri		= selectedImage;
                showPreviewBubble(cOverlay);
            }
        }
    }    
    
    private void populateMarkers() {
    	// Populates markers from database
    	ResourceImage[] photos	= photoData.getAll();
    	
    	for (ResourceImage ri: photos) {
    		PhotoRequest pr	=  ri.getPhotoRequest();
    		GeoPoint point = new GeoPoint(pr.getLat(), pr.getLon());
    		showMarker(point, pr.getResourceId(), stringToUri(pr.getResource()));    		
    	}
    	
//    	db	= new EmapixDB(this);
//    	PhotoRequestCursor cursor	= db.getPhotoRequests();
//    	// XXX: Retrieve data from server
//    	for (int i=0; i<cursor.getCount(); i++) {
//    		cursor.moveToPosition(i);
//    		GeoPoint point = new GeoPoint((int) cursor.getLat(), (int) cursor.getLon());
//    		showMarker(point, cursor.getId(), stringToUri(cursor.getResource()));
//    	}
    }
    
    private Uri stringToUri(String res) {
		if (isValidUri(res))
			return Uri.parse(res);    	
    	return null;
    }
    

    public static boolean isValidUri(String uri) {
    	// Checks if uri is valid. XXX: Move to some other class
    	if (uri == null)
    		return false;
    	
		String scheme	= Uri.parse(uri).getScheme(); // filter by scheme
		if (scheme == null)
			return false;
		
		return true;
    }
    
    private void sendRequest(GeoPoint point)
    {
    	// XXX: Send request to the server
    	bubble.setVisibility(View.GONE); 	// Close bubble
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
    	showMarker(point, id, null);
    }
    
    public void updateMarker(long id, Uri uri) {
    	db.updateMarker(id, String.format("%s", uri));
    	
    }
    
    public void showMarker(GeoPoint point, long id, Uri uri) {
    	Drawable marker = markers.get(getColor(uri));

    	// Show marker
    	OverlayItem item	= new OverlayItem(point, null, null);   
    	itemOverlay	= new MarkerOverlay(marker, this, point, id);
    	itemOverlay.addOverlay(item);
    	if (uri != null)
    		itemOverlay.setImage(getImageFromUri(uri));
    	mOverlays.add(itemOverlay);
    }
    
    private String getColor(Uri uri) {
    	if (isValidUri(String.format("%s", uri)))
    		return "blue";				
    	return "red";
    }
    
    private Bitmap getImageFromUri(Uri uri) {
    	if (uri == null)
    		return null;
    	
        String[] filePathColumn = {MediaStore.Images.Media.DATA};
        Cursor cursor = getContentResolver().query(uri, filePathColumn, null, null, null);

        cursor.moveToFirst();
        int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
        String filePath = cursor.getString(columnIndex);
        
        File f	= new File(filePath);
        currName	= new String(f.getName());	// Temp
        
        cursor.close();

        return BitmapFactory.decodeFile(filePath);    	
    }
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }  

}
    

//// XXX: Redo
//File imgFile = new  File("/sdcard/download/puppy1.jpg");
//
//if(imgFile.exists()){
//    Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
//    ImageView image = (ImageView) bubble.findViewById(R.id.bubble_image);
//    image.setImageBitmap(myBitmap);
//}        
//
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

