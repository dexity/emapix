package com.emapix;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.util.Log;

// XXX: Encapsulate data

// Database model class
class PhotoRequest
{
	private int lat;
	private int lon;
	private int resourceId;
	private String resource;
	private String submitted_date;
	
	public PhotoRequest() {}
	
	public PhotoRequest(int id, int lat, int lon, String resource, String date) {
		this.lat	= lat;
		this.lon	= lon;
		this.resourceId	= id;
		this.resource	= resource;
		this.submitted_date	= date;
	}
	// gets
	public int getLat() {return lat;}
	public int getLon() {return lon;}
	public int getResourceId() {return resourceId;}
	public String getResource() {return resource;}
	public String getDate() {return submitted_date;}

	// sets
	public void setLat(int lat) {this.lat 	= lat;}
	public void setLon(int lon) {this.lon	= lon;}
	public void setResource(String resource) {this.resource = resource;}
	public void setResourceId(int id) {resourceId = id;}
	public void setDate(String date) {submitted_date = date;}
	
	public String toString() {
		return String.format("lat = %s; lon = %s; resourceId = %s; resource = %s; date = %s", 
							 lat, lon, resourceId, resource, submitted_date);
	}	
}

// ResourceImage holds both model data and view data 

class ResourceImage 
{
	private PhotoRequest request;
	public Bitmap image;
	public String resourceUri;	// Http uri
	public Uri localUri;		// For caching?
	
	public ResourceImage() {}
	
	public void setPhotoRequest(PhotoRequest request) {this.request = request;}	
	public PhotoRequest getPhotoRequest() {return request;}	
	
	public void setBitmapUri(String uri) {
		//String _uri	= "https://s3.amazonaws.com/emapix_uploads/cern.jpg";
		try {
			URLConnection conn = new URL(uri).openConnection();
			BufferedInputStream bis	= new BufferedInputStream(conn.getInputStream());
			image 	= BitmapFactory.decodeStream(bis);
			resourceUri = uri;
		} catch (Exception e) {
			Log.e("setBitmapUri", e.toString());
		}
	}
	
	public String getResource() {
		try {
			return request.getResource();
		} catch (Exception e) {
			return "";
		}
	}
	
	public String toString() {
		return String.format("request = (%s); image = %s; resourceUri = %s; localUri = %s", 
							 request, image, resourceUri, localUri);
	}
	
	
}