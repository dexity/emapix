package com.emapix.layouts;

import com.emapix.R;

import android.app.Activity;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.os.Bundle;

public class LoginLoading extends Activity
{
	@Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.test_login_loading);
        ProgressDialog dialog = ProgressDialog.show(this, "", 
                							"Loading. Please wait...", true);  
        dialog.setCancelable(true);
        //showDialog(0);
    }	
    
//    @Override
//    protected Dialog onCreateDialog(int id) {
//        switch (id) {
//            case 0: {
//                ProgressDialog dialog = new ProgressDialog(this);
//                dialog.setMessage("Loading...");
//                dialog.setIndeterminate(true);
//                dialog.setCancelable(true);
//                return dialog;
//            }
//        }
//        return null;
//    }
}