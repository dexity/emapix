package com.emapix;

import android.content.Context;
import android.util.AttributeSet;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.google.android.maps.GeoPoint;
import com.google.android.maps.MapView;
import com.google.android.maps.OverlayItem;

// Not used for now

public class BubbleView<Item extends OverlayItem> extends FrameLayout {

	private LinearLayout layout;
	private TextView title;
	private Button btn_sendreq;
	private MapView mView;

	/**
	 * Create a new BubbleOverlayView.
	 * 
	 * @param context - The activity context.
	 * @param bubbleBottomOffset - The bottom padding (in pixels) to be applied
	 * when rendering this view.
	 */
	public BubbleView(Context context, MapView v, GeoPoint point, int bubbleBottomOffset) {
    	
		// Keep!
		super(context);

		mView	= v;
		setPadding(10, 0, 10, bubbleBottomOffset);
		
		layout = new LimitLinearLayout(context);
		layout.setVisibility(VISIBLE);

		setupView(context, layout);
		FrameLayout.LayoutParams params = new FrameLayout.LayoutParams(
				LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT);
		params.gravity = Gravity.NO_GRAVITY;

		addView(layout, params);

	}

	/**
	 * Inflate and initialize the BubbleOverlayView UI. Override this method
	 * to provide a custom view/layout for the bubble. 
	 * 
	 * @param context - The activity context.
	 * @param parent - The root layout into which you must inflate your view.
	 */
	protected void setupView(Context context, final ViewGroup parent) {
		
		LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		View v 		= inflater.inflate(R.layout.bubble, mView, false);
		title 		= (TextView) v.findViewById(R.id.locationname);
		btn_sendreq	= (Button) v.findViewById(R.id.sendreq);
		
	}
	
	/**
	 * Sets the view data from a given overlay item.
	 * 
	 * @param item - The overlay item containing the relevant view data. 
	 */
	public void setData(Item item) {
		layout.setVisibility(VISIBLE);
		setBubbleData(item, layout);
	}
	
	/**
	 * Sets the view data from a given overlay item. Override this method to create
	 * your own data/view mappings.
	 * 
	 * @param item - The overlay item containing the relevant view data.
	 * @param parent - The parent layout for this BubbleOverlayView.
	 */
	protected void setBubbleData(Item item, ViewGroup parent) {
		if (item.getTitle() != null) {
			title.setVisibility(VISIBLE);
			title.setText(item.getTitle());
		} else {
			title.setText("");
			title.setVisibility(GONE);
		}
		btn_sendreq.setVisibility(VISIBLE);
		Log.i("SET_BUBBLE", item.getTitle());
	}
	
	private class LimitLinearLayout extends LinearLayout {

	    private static final int MAX_WIDTH_DP = 280;
	    
	    final float SCALE = getContext().getResources().getDisplayMetrics().density;

	    public LimitLinearLayout(Context context) {
	        super(context);
	    }

	    public LimitLinearLayout(Context context, AttributeSet attrs) {
	        super(context, attrs);
	    }

	    @Override
	    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
	        int mode = MeasureSpec.getMode(widthMeasureSpec);
	        int measuredWidth = MeasureSpec.getSize(widthMeasureSpec);
	        int adjustedMaxWidth = (int)(MAX_WIDTH_DP * SCALE + 0.5f);
	        int adjustedWidth = Math.min(measuredWidth, adjustedMaxWidth);
	        int adjustedWidthMeasureSpec = MeasureSpec.makeMeasureSpec(adjustedWidth, mode);
	        super.onMeasure(adjustedWidthMeasureSpec, heightMeasureSpec);
	    }
	}

}
