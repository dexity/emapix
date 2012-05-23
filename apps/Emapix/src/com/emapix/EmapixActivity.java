
package com.emapix;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
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
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
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
import android.widget.Toast;

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

// XXX: Cannot load more than 4 large pictures. Resources are not released?
// XXX: Refactor Uri to separate local uri and remove uri.

/*
 * Notes:
 * 		- All images are uploaded from a local storage
 * 		- When completed request gets removed, both record and S3 image (TODO) gets removed
 */

public class EmapixActivity extends MapActivity {
	
	private LinearLayout bubble;
	private EmapixMapView mView;
	//private IPhotoData photoData;
	private ServicePhotoData photoData;
	private MarkerOverlay cOverlay;
	private MarkerOverlay itemOverlay;
	List<Overlay> mOverlays;
	HashMap<String, Drawable> markers;
	ResourceImage crImage;	// current resource image
	Menu mMenu;
	
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

		photoData	= new ServicePhotoData(this); // new LocalPhotoData(this);		
    	mOverlays 	= mView.getOverlays();
    	crImage		= new ResourceImage();	// create current resource image
    	
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
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {   
        // Hold on to this
        mMenu = menu;
        
        // Inflate the currently selected menu XML resource.
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);        
                
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        
        switch (item.getItemId()) {
            case R.id.refresh:
            	refreshMap();
                Toast.makeText(this, "Refreshed", Toast.LENGTH_SHORT).show();
                return true;              
        }
        return false;
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
    
    public void showCurrOverlay() {
    	mOverlays.add(cOverlay);	
    }
    
    public void hideCurrOverlay(MarkerOverlay currOverlay) {
    	// Hide current overlay
    	cOverlay = currOverlay;
    	mOverlays.remove(currOverlay);	
    }
    
    public void cleanupBubbles() {
        // Removes bubble  
    	mView.removeAllViews();
    	
    	if (bubble != null)
    		bubble.setVisibility(View.GONE);
    }
    
    private LinearLayout bubbleFactory(int resource, GeoPoint point) {
        LayoutInflater inflater = (LayoutInflater) getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        LinearLayout layout = (LinearLayout) inflater.inflate(resource, mView, false);

    	EmapixMapView.LayoutParams params = new EmapixMapView.LayoutParams(
		                		370, LayoutParams.WRAP_CONTENT,
		                 		point, EmapixMapView.LayoutParams.BOTTOM_CENTER);
    	params.mode = MapView.LayoutParams.MODE_MAP;
    	layout.setLayoutParams(params);    	
        return layout;
    }
    
    
    // Bubbles
    public void showRequestBubble(final GeoPoint point) {
        // Sets request bubble
    	cleanupBubbles(); 
    	
    	bubble	= bubbleFactory(R.layout.bubble, point);

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
    
        
    public void showActionBubble(MarkerOverlay currOverlay) {

    	GeoPoint point = currOverlay.getPoint();
        cleanupBubbles();
    	hideCurrOverlay(currOverlay);
    	
    	bubble	= bubbleFactory(R.layout.action_bubble, point);
        
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
            	photoData.remove((int)cOverlay.getId());
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
    
    
    public void showPreviewBubble(MarkerOverlay currOverlay) {
    	// Shows preview bubble. File is not submitted and resource is not set yet. 
    	// XXX: Add cache
    	GeoPoint point = currOverlay.getPoint();
    	cleanupBubbles();

    	bubble	= bubbleFactory(R.layout.preview_bubble, point);
    	
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
        if (crImage.image != null) {
			ImageView image = (ImageView) bubble.findViewById(R.id.bubble_image);
			image.setImageBitmap(crImage.image);        	
        }
        
        // Set submit button
        Button btn_submit	= (Button) bubble.findViewById(R.id.submit_pic);
        btn_submit.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
            	// XXX: Submitting pic to server
            	
            	// Show blue marker            	
            	showMarker(cOverlay.getPoint(), cOverlay.getId(), crImage.localUri, cOverlay.getResource());
            	//updateMarker(cOverlay.getId(), crImage.localUri);
            	cOverlay.setImage(crImage.image);
            	
            	bubble.setVisibility(View.GONE);
            	
            	// Submit to S3
            	submitImage(crImage.image);
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
            	// marker

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
    	// XXX: Add cache
        // Sets request bubble
    	GeoPoint point = currOverlay.getPoint();
    	cleanupBubbles(); 
    	hideCurrOverlay(currOverlay);
    	
    	bubble	= bubbleFactory(R.layout.view_bubble, point);
    	
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
            	
            	//updateMarker(cOverlay.getId(), null);
            	//showMarker(cOverlay.getPoint(), cOverlay.getId(), null, null);
            	// XXX: Need to remove image from S3
            	photoData.remove((int)cOverlay.getId());
            	bubble.setVisibility(View.GONE);            	
            }
        });
        
        
        if (mView.findViewById(bubble.getId()) == null)
        	mView.addView(bubble);
    	mView.measure(MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED), 
    				 MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED));
    	
    	bubble.setVisibility(View.VISIBLE);   	
    }

    
    private void submitImage(Bitmap bm) {
    	// Submits image to the server
    	
    	// XXX: Check if bitmap is JPEG or PNG
    	// XXX: Add parameter: resource=<resource>
    	String uri = String.format("%s/upload?key=%s", getString(R.string.base_uri), 
    											getString(R.string.api_key));
    	
    	try {
			ByteArrayOutputStream bos = new ByteArrayOutputStream();
			bm.compress(CompressFormat.JPEG, 75, bos);	// Fix compression format
			byte[] data = bos.toByteArray();
			// Http client
			HttpClient httpClient = new DefaultHttpClient();
			HttpPost postRequest = new HttpPost(uri);
			ByteArrayBody bab = new ByteArrayBody(data, cOverlay.getResource()+".jpg"); // Hope, resource is set	//currName);	// XXX: Fix filename

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
    
    
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent imageReturnedIntent) { 
        super.onActivityResult(requestCode, resultCode, imageReturnedIntent); 

        switch(requestCode) { 
        case PICK_IMAGE_CODE:
        	// Local image
            if(resultCode == RESULT_OK){  
                Uri selectedImage 	= imageReturnedIntent.getData();
                crImage.image 		= getImageFromFile(selectedImage);
                crImage.localUri	= selectedImage;
                showPreviewBubble(cOverlay);
            }
        }
    }    
    
    private void refreshMap() {
    	mOverlays.clear();
    	populateMarkers();
    	mView.invalidate();
    }
    
    private void populateMarkers() {
    	// Populates markers from database
    	ResourceImage[] photos	= photoData.getAll();
    	
    	for (ResourceImage ri: photos) {
    		PhotoRequest pr	=  ri.getPhotoRequest();
    		GeoPoint point = new GeoPoint(pr.getLat(), pr.getLon());
    		showMarker(point, pr.getResourceId(), 
    				   stringToUri(photoData.getFullUri(pr.getResource())), pr.getResource());    		
    	}
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
    	bubble.setVisibility(View.GONE); 	// Close bubble
    	addMarker(point);
    }
    
    public IPhotoData getPhotoData() {
    	return photoData;
    }
    
    public EmapixMapView getMapView() {
    	return mView;
    }
    
    public void addMarker(GeoPoint point) {
    	// Adds record to service
    	ResourceImage ri = photoData.add(point.getLatitudeE6(), point.getLongitudeE6());
    	showMarker(point, ri.getPhotoRequest().getResourceId(), null, ri.getResource());
    }
    
    public void updateMarker(long id, Uri uri) {
    	photoData.setResource((int)id, uri.toString());
    }
    
    //
    public void showMarker(GeoPoint point, long id, Uri uri, String resource) {
    	// Creates and sets overlay on the map
    	Bitmap im = null;
    	if (uri != null)
    		im	= getImage(uri);	// XXX: Dirty way of setting color
    	String color	= "red";
    	if (im != null)
    		color	= "blue";
    	Drawable marker = markers.get(color);

    	// Show marker  
    	itemOverlay	= new MarkerOverlay(marker, this, point, id, resource);	// The only place where the MarkerOverlay is created
    	itemOverlay.addOverlay(new OverlayItem(point, null, null));
    	if (im != null)
    		itemOverlay.setImage(im);
    	mOverlays.add(itemOverlay);
    }
    
    private String getColor(Uri uri) {
    	// Not used
		String scheme	= uri.getScheme(); // filter by scheme
		if (scheme.equals("https") || scheme.equals("http"))
    		return "blue";				
    	return "red";
    }
    
    private Bitmap getImage(Uri uri) {
		String scheme	= uri.getScheme(); // filter by scheme
		if (scheme.equals("https") || scheme.equals("http"))
			return getImageFromServer(uri);
		return getImageFromFile(uri);
    }
    
    private Bitmap getImageFromFile(Uri uri) {
    	// Returns bitmap object from the file uri
    	if (uri == null)
    		return null;
    	
        String[] filePathColumn = {MediaStore.Images.Media.DATA};
        Cursor cursor = getContentResolver().query(uri, filePathColumn, null, null, null);
        cursor.moveToFirst();
        int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
        String filePath = cursor.getString(columnIndex);        
        cursor.close();

        return BitmapFactory.decodeFile(filePath);    	
    }
   
    
    private Bitmap getImageFromServer(Uri uri) {
    	// Returns bitmap object from http uri
		try {
			URLConnection conn = new URL(uri.toString()).openConnection();
			BufferedInputStream bis	= new BufferedInputStream(conn.getInputStream());
			return BitmapFactory.decodeStream(bis);
		} catch (Exception e) {
			Log.e("getImageFromServer", e.toString());
			return null;
		}
    }
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }  

}
   



