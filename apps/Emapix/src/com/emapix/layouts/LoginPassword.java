package com.emapix.layouts;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;

import com.emapix.R;

public class LoginPassword extends Activity
{
	@Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.test_login_loading);
        Dialog dialog	= new AlertDialog.Builder(this)
        .setIcon(R.drawable.alert_dialog_icon)
        .setTitle("Incorrect Password")
        .setMessage("The password you entered is incorrect. Please try again")
        .setPositiveButton("OK", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                /* User clicked OK so do some stuff */
            }
        })
        .create();
        dialog.setCancelable(true);
        dialog.show();
    }	
}