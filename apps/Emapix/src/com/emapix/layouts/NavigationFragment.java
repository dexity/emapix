
package com.emapix.layouts;

import com.actionbarsherlock.app.SherlockFragment;
import com.emapix.R;

import android.app.Activity;
import android.os.Bundle;
import android.util.AttributeSet;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;


public class NavigationFragment extends SherlockFragment {

	public static final String TAG = "navFragment";
	private static final int ACTIVE = 0xFFBBBBBB;
	public NavigationFragment() {}
	
	protected TextView map;
	protected TextView req;
	protected TextView photo;
	protected TextView filter;
	private int activeTab = -1;
	
	@Override
	public void onCreate(Bundle arg0) {
		super.onCreate(arg0);
		setRetainInstance(true);
	}
	
	private View.OnClickListener getListener() {
		
		return new View.OnClickListener() {			
			@Override
			public void onClick(View v) {
				Toast.makeText(NavigationFragment.this.getActivity(), 
							  ((TextView)v).getText(), Toast.LENGTH_SHORT).show();				
			}
		};
	}
	
	public void setTabActive(int order) {
		activeTab	= order;
	}
	
	private void setTab() {
		switch (activeTab) {
			case 0:
				map.setBackgroundColor(ACTIVE);
				break;
			case 1:
				req.setBackgroundColor(ACTIVE);
				break;
			case 2:
				photo.setBackgroundColor(ACTIVE);
				break;
			case 3:
				filter.setBackgroundColor(ACTIVE);
				break;
		}
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup vg, Bundle data) {
		View v	= (View)inflater.inflate(R.layout.test_navigation, vg, false);
		
        // Set clicks for navigation 
        map	= (TextView)v.findViewById(R.id.nav_map);
        map.setOnClickListener(getListener());			

        req	= (TextView)v.findViewById(R.id.nav_request);
        req.setOnClickListener(getListener());			

        photo	= (TextView)v.findViewById(R.id.nav_photo);
        photo.setOnClickListener(getListener());			        
        
        filter	= (TextView)v.findViewById(R.id.nav_search);
        filter.setOnClickListener(getListener());			
        
        setTab();      
        
		return v;
	}
}	
