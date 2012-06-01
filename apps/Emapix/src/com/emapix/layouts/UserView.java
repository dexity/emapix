package com.emapix.layouts;

import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.actionbarsherlock.app.SherlockFragment;
import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.emapix.R;

public class UserView extends SherlockFragmentActivity
{
	private NavigationFragment navFragment;
	private UserViewFragment photoFragment;
	
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
        	ft.add(R.id.navigation, navFragment, NavigationFragment.TAG);
        }
        
        photoFragment = (UserViewFragment) getSupportFragmentManager().findFragmentByTag(UserViewFragment.TAG);
        if (photoFragment == null) {
        	photoFragment = new UserViewFragment(this);
        	ft.add(R.id.fragment_container, photoFragment, UserViewFragment.TAG);
        }
        ft.commit();
	}   
	
    public class UserViewFragment extends SherlockFragment
    {
    	public static final String TAG = "userViewFragment";	
    	private Context mContext;
    	 
    	public UserViewFragment(Context context){mContext = context;}
    	
    	@Override
    	public View onCreateView(LayoutInflater inflater, ViewGroup vg, Bundle data) {
    		
    		LinearLayout ll	= (LinearLayout)inflater.inflate(R.layout.test_user_view, vg, false);
    		((TextView)ll.findViewById(R.id.username)).setText("dexity");
    		((TextView)ll.findViewById(R.id.name)).setText("Alex Dementsov");
    		((TextView)ll.findViewById(R.id.join_time)).setText("May 18 2012, 5:13pm");
    		((TextView)ll.findViewById(R.id.request_count)).setText("34");
    		((TextView)ll.findViewById(R.id.photo_count)).setText("12"); 
    		return ll;
    	}
    }
    
    @Override
    protected boolean isRouteDisplayed() {
        return false;
    }    
}