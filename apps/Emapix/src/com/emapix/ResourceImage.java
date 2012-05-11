package com.emapix;

import android.graphics.Bitmap;
import android.net.Uri;

class ResourceImage 
{
	public Bitmap image;
	public String resourceUri;
	public String resourceId;
	public Uri localUri;
	
	public ResourceImage(Bitmap image, String resource, Uri uri) {
		this.image		= image;
		this.resourceUri = resource;
		this.localUri	= uri;
	}
	
}