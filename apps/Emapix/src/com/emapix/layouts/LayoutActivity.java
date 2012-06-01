// Displays layouts

package com.emapix.layouts;

import java.util.HashMap;

import com.actionbarsherlock.app.SherlockListActivity;
import com.emapix.R;


import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.AttributeSet;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.LinearLayout.LayoutParams;


public class LayoutActivity extends SherlockListActivity {
    /** Called when the activity is first created. */
	SimpleListAdapter adapter;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        adapter	= new SimpleListAdapter(this);
        setListAdapter(adapter);
    }
    
    private class SimpleListAdapter extends BaseAdapter {
    	
    	private Context mContext;
    	private HashMap<Integer, StringClass> mLayouts;
    	
        private class StringClass {
        	String name;
        	Class cls;   
        	public StringClass(String name, Class cls) {
        		this.name	= name;
        		this.cls	= cls;
        	}
        }
            
        public SimpleListAdapter(Context context) {
            mContext = context;
            setItems();
        }
        
        public Class getClass(int position) {
        	return mLayouts.get(position).cls;
        }
        
        public void setItems() {
        	mLayouts	= new HashMap<Integer, StringClass>();
    		mLayouts.put(0, new StringClass("+ Login view", LoginView.class));
    		mLayouts.put(1, new StringClass("+ Login loading", LoginLoading.class));
    		mLayouts.put(2, new StringClass("+ Incorrect password", LoginPassword.class));
    		mLayouts.put(3, new StringClass("+ Main view", MarkerView.class));
    		mLayouts.put(4, new StringClass("+ Request bubble", RequestBubble.class));
    		mLayouts.put(5, new StringClass("+ Action bubble", ActionBubble.class));
    		mLayouts.put(6, new StringClass("+ Preview bubble", PreviewBubble.class));
    		mLayouts.put(7, new StringClass("+ View bubble", ViewBubble.class));
    		mLayouts.put(8, new StringClass("+ Requests list", RequestList.class));
    		mLayouts.put(9, new StringClass("+ Request view", RequestView.class));
    		mLayouts.put(10, new StringClass("+ Photo list", PhotoList.class));
    		mLayouts.put(11, new StringClass("+ Photo view", PhotoView.class));
    		mLayouts.put(12, new StringClass("+ User view", UserView.class));   	
        }
        
        public View getView(int position, View convertView, ViewGroup parent) {
        	TextView tv	= (TextView)View.inflate(mContext, R.layout.test_list_item, null);
        	tv.setText(mLayouts.get(position).name);
        	return tv;
        }
        
        public int getCount() {
        	return mLayouts.size();
        }
        
        public Object getItem(int position) {
            return position;
        }
        
        public long getItemId(int position) {
            return position;
        }        
    }
    
    @Override
    protected void onListItemClick(ListView l, View v, int position, long id) {
		// Show map view
	    Intent intent = new Intent();
	    intent.setClass(this, adapter.getClass(position));
	    startActivity(intent);

    }
    
}