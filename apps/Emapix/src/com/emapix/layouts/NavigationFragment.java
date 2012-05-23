
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
	public NavigationFragment() {}
	
	private TextView req;
	private TextView photo;
	private TextView filter;
	
	@Override
	public void onCreate(Bundle arg0) {
		super.onCreate(arg0);
		setRetainInstance(true);
		
	}
	
	private View.OnClickListener getListener() {
		
		return new View.OnClickListener() {			
			@Override
			public void onClick(View v) {
				Toast.makeText(NavigationFragment.this.getActivity(), ((TextView)v).getText(), Toast.LENGTH_SHORT).show();				
			}
		};
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup vg, Bundle data) {
		View v	= (View)inflater.inflate(R.layout.test_navigation, vg, false);
		
        // Set clicks for navigation 
        req	= (TextView)v.findViewById(R.id.nav_request);
        req.setOnClickListener(getListener());			

        photo	= (TextView)v.findViewById(R.id.nav_photo);
        photo.setOnClickListener(getListener());			        
        
        filter	= (TextView)v.findViewById(R.id.nav_filter);
        filter.setOnClickListener(getListener());			
        
		return v;
	}
}	

//public class NavigationFragment extends Fragment {
//	
//    static NavigationFragment newInstance(int index) {
//        return new NavigationFragment();
//    }	
//	
//    @Override 
//    public void onInflate(Activity activity, AttributeSet attrs,
//            Bundle savedInstanceState) {
//        super.onInflate(activity, attrs, savedInstanceState);
//    }
//    
//    @Override
//    public View onCreateView(LayoutInflater inflater, ViewGroup container,
//                             Bundle savedInstanceState) {
//        TextView tv	= new TextView(getActivity());
//        tv.setText("Hello");
//        tv.setHeight(50);
//    	return tv;
//    	// Inflate the layout for this fragment
//        //return inflater.inflate(R.layout.test_control_fragment, container, false);
//    	
//    }
//}