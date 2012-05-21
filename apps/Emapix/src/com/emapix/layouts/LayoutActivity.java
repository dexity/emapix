// Displays layouts

package com.emapix.layouts;

import org.xmlpull.v1.XmlPullParser;

import com.emapix.R;

import android.app.Activity;
import android.app.ListActivity;
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


public class LayoutActivity extends ListActivity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setListAdapter(new SimpleListAdapter(this));
    }
    
    private class SimpleListAdapter extends BaseAdapter {
    	
    	private Context mContext;
    	private String[] mLayouts = {
    		"Login view",
    		"Login loading",
    		"Incorrect password",
    		"Main view",
    		"Mapker on map",
    		"Request bubble",
    		"Action bubble",
    		"Preview bubble",
    		"View bubble",
    		"Requests list",
    		"Request details",
    		"Photo list",
    		"Photo details",
    		"User details",
    		"Filter"
    	};
    	
    
        public SimpleListAdapter(Context context) {
            mContext = context;
        }
        
        public View getView(int position, View convertView, ViewGroup parent) {
        	TextView tv	= (TextView)View.inflate(mContext, R.layout.test_text, null);
        	tv.setText(mLayouts[position]);
        	return tv;
        }
        
        public int getCount() {
        	return mLayouts.length;
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
	    intent.setClass(this, MainView.class);
	    startActivity(intent);

    }
    
}