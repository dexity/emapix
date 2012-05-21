// Displays layouts

package com.emapix.layouts;

import org.xmlpull.v1.XmlPullParser;

import com.emapix.R;

import android.app.Activity;
import android.app.ListActivity;
import android.content.Context;
import android.os.Bundle;
import android.util.AttributeSet;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
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
    		"Hello",
    		"world"
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
    
}