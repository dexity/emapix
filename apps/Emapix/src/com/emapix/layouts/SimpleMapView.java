package com.emapix.layouts;

import android.content.Context;
import android.util.AttributeSet;

import com.google.android.maps.MapView;

public class SimpleMapView extends MapView {

	public SimpleMapView(Context context, String apiKey) {
		super(context, apiKey);
	}

	public SimpleMapView(Context context, AttributeSet attrs) {
		super(context, attrs);
	}

	public SimpleMapView(Context context, AttributeSet attrs, int defStyle) {
		super(context, attrs, defStyle);
	}
}