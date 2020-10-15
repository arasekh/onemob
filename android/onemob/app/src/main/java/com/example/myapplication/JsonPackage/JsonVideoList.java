package com.example.myapplication.JsonPackage;

import android.os.AsyncTask;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Request.Builder;

public class JsonVideoList extends AsyncTask {
    @Override
    protected Object doInBackground(Object[] objects) {
        OkHttpClient client = new OkHttpClient.Builder().build();
        Request request = new Request.Builder().url("").method("GET", null).build();
        return null;
    }
}
