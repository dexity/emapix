package com.emapix.layouts;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.actionbarsherlock.app.SherlockListFragment;
import com.emapix.R;

public class RequestList extends SherlockFragmentActivity
{
	private NavigationFragment navFragment;
	private RequestFragment reqFragment;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_map_view);
        
        setupFragments();
    }
    
	private void setupFragments() {
		final FragmentTransaction ft = getSupportFragmentManager()
									   .beginTransaction();

		navFragment	= (NavigationFragment) getSupportFragmentManager().findFragmentByTag(NavigationFragment.TAG);
        if (navFragment == null) {
        	navFragment = new NavigationFragment();
        	navFragment.setTabActive(0);
        	ft.add(R.id.navigation, navFragment, NavigationFragment.TAG);
        }
        
        reqFragment = (RequestFragment) getSupportFragmentManager().findFragmentByTag(RequestFragment.TAG);
        if (reqFragment == null) {
        	reqFragment = new RequestFragment(this);
        	ft.add(R.id.fragment_container, reqFragment, RequestFragment.TAG);
        }
        ft.commit();
	}    
    
    public class RequestFragment extends SherlockListFragment
    {
    	public static final String TAG = "reqFragment";
    	Context mContext;
    	
    	public RequestFragment(Context context){mContext = context;}
    	
        @Override
        public void onActivityCreated(Bundle savedInstanceState) {
            super.onActivityCreated(savedInstanceState);
            setListAdapter(new RequestListAdapter(mContext));
        }
            	
	    private class RequestListAdapter extends BaseAdapter {
	    	
	    	private Context mContext;	    	
	        
	        public RequestListAdapter(Context context) {
	            mContext = context;
	        }
	        
	        public View getView(int position, View convertView, ViewGroup parent) {
	        	LinearLayout ll	= (LinearLayout)View.inflate(mContext, R.layout.test_request_item, null);
	        	((TextView)ll.findViewById(R.id.username)).setText("dexity");
	        	((TextView)ll.findViewById(R.id.time)).setText("May 18 2012, 5:13pm");
	        	((TextView)ll.findViewById(R.id.description)).setText("Planning to hike in this place ...");        	
	        	return ll; 
	        }
	        
	        public int getCount() {
	        	return 10;	//mLayouts.length;
	        }
	        
	        public Object getItem(int position) {
	            return position;
	        }
	        
	        public long getItemId(int position) {
	            return position;
	        }        
	    }
    }
}