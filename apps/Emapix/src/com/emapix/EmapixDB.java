package com.emapix;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteCursor;
import android.database.sqlite.SQLiteCursorDriver;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteQuery;
import android.util.Log;


// Note: I don't care about the record _id, just res_id 

public class EmapixDB extends SQLiteOpenHelper {

    private static final String DATABASE_NAME = "Emapix";
    private static final int DATABASE_VERSION = 1;
    private final Context mContext;	
	
    public EmapixDB(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        this.mContext = context;
	}	
	
    // Cursor
	public static class PhotoRequestCursor extends SQLiteCursor {
    	private static final String QUERY = 
        		"SELECT _id, res_id, lat, lon, submitted_date, resource "+
        	    "FROM photo_request";
    	private static final String QUERY_ID = 
        		"SELECT _id, res_id, lat, lon, submitted_date, resource "+
        	    "FROM photo_request " +
        		"WHERE res_id=%s";
	    private PhotoRequestCursor(SQLiteDatabase db, SQLiteCursorDriver driver,
								   String editTable, SQLiteQuery query) {
			super(db, driver, editTable, query);
		}
	    private static class Factory implements SQLiteDatabase.CursorFactory {
			public Cursor newCursor(SQLiteDatabase db,
					SQLiteCursorDriver driver, String editTable,
					SQLiteQuery query) {
				return new PhotoRequestCursor(db, driver, editTable, query);
			}
	    }
	    
	    public int getLat(){return getInt(getColumnIndexOrThrow("lat"));}
	    public int getLon(){return getInt(getColumnIndexOrThrow("lon"));}
	    public int getId(){return getInt(getColumnIndexOrThrow("_id"));}
	    public int getResId(){return getInt(getColumnIndexOrThrow("res_id"));}
	    public String getDate(){return getString(getColumnIndexOrThrow("submitted_date"));}
	    public String getResource(){return getString(getColumnIndexOrThrow("resource"));}
	}
	
	// Refactor update methods?
	public void updateResId(long id) {
		ContentValues map = new ContentValues();
		map.put("res_id", id);
		String[] whereArgs = new String[]{Long.toString(id)};
		try{
			getWritableDatabase().update("photo_request", map, "_id=?", whereArgs);
		} catch (SQLException e) {
            Log.e("Error writing new job", e.toString());
		}
	}	
	
	public void updateMarker(long res_id, String resource) {
		ContentValues map = new ContentValues();
		map.put("resource", resource);
		String[] whereArgs = new String[]{Long.toString(res_id)};
		try{
			getWritableDatabase().update("photo_request", map, "res_id=?", whereArgs);
		} catch (SQLException e) {
            Log.e("Error writing new job", e.toString());
		}
	}
	
    private void execMultipleSQL(SQLiteDatabase db, String[] sql){
    	for( String s : sql )
    		if (s.trim().length()>0)
    			db.execSQL(s);
    }	
	
    public long addRequest(int lat, int lon) {
		ContentValues map = new ContentValues();
		map.put("lat", lat);
		map.put("lon", lon);
		try{
			return getWritableDatabase().insert("photo_request", null, map);
		} catch (SQLException e) {
            Log.e("Error writing new photo_request", e.toString());
		}
		return -1;
    }
    
    public void deleteRequest(long res_id) {
		String[] whereArgs = new String[]{Long.toString(res_id)};
		try{
			getWritableDatabase().delete("photo_request", "res_id=?", whereArgs);
		} catch (SQLException e) {
            Log.e("Error deleteing photo_request", e.toString());
		}    	
    }
    
    public PhotoRequestCursor getPhotoRequests() {
    	SQLiteDatabase d = getReadableDatabase();
    	PhotoRequestCursor c = (PhotoRequestCursor) d.rawQueryWithFactory(
			new PhotoRequestCursor.Factory(),
			PhotoRequestCursor.QUERY,
			null,
			null);
    	c.moveToFirst();
        return c;
    }    
    
	public PhotoRequestCursor getPhotoRequest(int res_id) {
		// Returns record specified by res_id
		SQLiteDatabase d = getReadableDatabase();
    	PhotoRequestCursor c = (PhotoRequestCursor) d.rawQueryWithFactory(
			new PhotoRequestCursor.Factory(),
			String.format(PhotoRequestCursor.QUERY_ID, res_id),
			null,
			null);
    	c.moveToFirst();
        return c;		
	}
    
    
	@Override
	public void onCreate(SQLiteDatabase db) {
		String[] sql = mContext.getString(R.string.EmapixDB_onCreate).split("\n");
		db.beginTransaction();
		try {
			// Create tables & test data
			execMultipleSQL(db, sql);
			db.setTransactionSuccessful();
		} catch (SQLException e) {
            Log.e("Error creating tables and debug data", e.toString());
        } finally {
        	db.endTransaction();
        }		
	}
	
	@Override
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
		String[] sql = mContext.getString(R.string.EmapixDB_onUpgrade).split("\n");
		db.beginTransaction();
		try {
			// Create tables & test data
			execMultipleSQL(db, sql);
			db.setTransactionSuccessful();
		} catch (SQLException e) {
            Log.e("Error creating tables and debug data", e.toString());
        } finally {
        	db.endTransaction();
        }

        // This is cheating.  In the real world, you'll need to add columns, not rebuild from scratch
        onCreate(db);	
	}
}