package com.emapix.layouts;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.actionbarsherlock.app.SherlockListActivity;
import com.actionbarsherlock.app.SherlockListFragment;
import com.emapix.R;

public class PhotoList extends SherlockFragmentActivity
{
	private NavigationFragment navFragment;
	private PhotoFragment reqFragment;
	
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
        	navFragment.setTabActive(1);
        	ft.add(R.id.navigation, navFragment, NavigationFragment.TAG);
        }
        
        reqFragment = (PhotoFragment) getSupportFragmentManager().findFragmentByTag(PhotoFragment.TAG);
        if (reqFragment == null) {
        	reqFragment = new PhotoFragment(this);
        	ft.add(R.id.fragment_container, reqFragment, PhotoFragment.TAG);
        }
        ft.commit();
	}    
    
    public class PhotoFragment extends SherlockListFragment
    {
    	public static final String TAG = "reqFragment";
    	Context mContext;
    	
    	public PhotoFragment(Context context){mContext = context;}
    	
        @Override
        public void onActivityCreated(Bundle savedInstanceState) {
            super.onActivityCreated(savedInstanceState);
            setListAdapter(new PhotoListAdapter(mContext));
        }
            	
	    private class PhotoListAdapter extends BaseAdapter {
	    	
	    	private Context mContext;	    	
	        
	        public PhotoListAdapter(Context context) {
	            mContext = context;
	        }
	        
	        public View getView(int position, View convertView, ViewGroup parent) {
	        	LinearLayout ll	= (LinearLayout)View.inflate(mContext, R.layout.test_photo_item, null);
	        	((TextView)ll.findViewById(R.id.username)).setText("dexity");
	        	((TextView)ll.findViewById(R.id.time)).setText("May 18 2012, 5:13pm");
	        	((TextView)ll.findViewById(R.id.req_username)).setText("lunatix");
	        	return ll; 
	        }
	        
	        public int getCount() {
	        	return 10;
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