package com.emapix;

import android.graphics.Bitmap;
import android.net.Uri;

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
	
	public PhotoRequest(int lat, int lon, int id, String resource, String date) {
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
}

//
class ResourceImage 
{
	private PhotoRequest request;
	public Bitmap image;
	public String resourceUri;	// global uri
	public Uri localUri;
	
	public ResourceImage() {}
	public ResourceImage(Bitmap image, String resource, Uri uri) {
		this.image		= image;
		this.resourceUri = resource;
		this.localUri	= uri;
	}
	
	public void setPhotoRequest(PhotoRequest request) {this.request = request;}	
	public PhotoRequest getPhotoRequest() {return request;}	
}