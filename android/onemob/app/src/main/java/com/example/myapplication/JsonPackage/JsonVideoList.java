package com.example.myapplication.JsonPackage;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import com.example.myapplication.R;
import com.example.myapplication.ShowVideoActivity;
import com.example.myapplication.Video;
import com.example.myapplication.VideoListAdapter;
import com.example.myapplication.ui.videos.VideosFragment;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class JsonVideoList extends AsyncTask {

    ArrayList<JSONObject> videosJsonObjectArrayList = new ArrayList<>();
    String[] videosName = null;
    String[] videosTitle = null;
    String token;
    Activity activity = null;
    Context context = null;
    ListView videosListView;
    String path;
    File file;

    public JsonVideoList(String token, Context context, Activity activity, ListView videosListView) {
        this.token = token;
        this.context = context;
        this.activity = activity;
        this.videosListView = videosListView;
    }

    public JsonVideoList(String token) {
        this.token = token;
    }

    public JsonVideoList(String token, Activity activity, ListView videosListView) {
        this.token = token;
        this.activity = activity;
        this.videosListView = videosListView;
    }

    @Override
    protected Object doInBackground(Object[] objects) {
        try {
            path = "/storage/emulated/0/OneMob";
            file = new File(path);
            if (!file.exists()){
                file.mkdirs();
                Log.d("FILE EXISTS", file.getAbsolutePath());
            }
            OkHttpClient client = new OkHttpClient.Builder().build();
            Request request = new Request.Builder().url("http://192.168.1.5:8000/api/videos").method("GET", null).addHeader("Authorization", "Token "+token).build();
            Response response = null;
            String resultVideoList = "";
            JSONObject jsonObject = null;
            JSONArray jsonArray = null;
            JSONObject video1 = null;
            String video1Name = "";
            int jsonArrayLength = 0;
            try {
                response = client.newCall(request).execute();
                resultVideoList = response.body().string();
                jsonObject = new JSONObject(resultVideoList);
                jsonArray = jsonObject.getJSONArray("videos");
                jsonArrayLength = jsonArray.length();

                videosName = new String[jsonArrayLength];
                for (int i = 0 ; i < jsonArrayLength ; i++){
                    videosJsonObjectArrayList.add(jsonArray.getJSONObject(i));
                }
                for (int j = 0 ; j < videosJsonObjectArrayList.size() ; j++){
                    videosName[j] = videosJsonObjectArrayList.get(j).getString("name");
                }

                videosTitle = new String[jsonArrayLength];
                for (int l = 0 ; l < jsonArrayLength ; l++){
                    videosTitle[l] = videosJsonObjectArrayList.get(l).getString("title");
                }
                video1 = jsonArray.getJSONObject(0);
                video1Name = video1.getString("name");
            } catch (IOException | JSONException e) {
                e.printStackTrace();
            }
            Log.d("token", token);
            Log.d("resultVideoList", resultVideoList);
            Log.d("JsonObject", String.valueOf(jsonObject));
            Log.d("videosArray", String.valueOf(jsonArray));
            Log.d("video1", String.valueOf(video1));
            Log.d("video1Name", video1Name);
            Log.d("jsonArrayLength", String.valueOf(jsonArrayLength));
            for (int k = 0 ; k < videosName.length ; k++){
                Log.d("VideosName", videosName[k]);
            }
            for (int z = 0 ; z < videosTitle.length ; z++){
                Log.d("VideosTitle", videosTitle[z]);
            }
        } catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(Object o) {
        super.onPostExecute(o);
        try {
            int fileCount = videosName.length;
            Log.d("fileCount", String.valueOf(fileCount));
            ArrayList<Video> videosList = genVideos(fileCount, videosName);
            VideoListAdapter adapter = new VideoListAdapter(activity, R.layout.videos_view_layout, videosList);
            videosListView.setAdapter(adapter);
            videosListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                @Override
                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                    JsonVideosDownload jsonVideosDownloadList = new JsonVideosDownload(token, videosTitle[position]);
                    Intent toShowVideo = new Intent(context, ShowVideoActivity.class);
                    toShowVideo.putExtra("tokenShowVideo", token);
                    toShowVideo.putExtra("VideoTitleList", videosTitle[position]);
                    context.startActivity(toShowVideo);
                }
            });
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public int getFileCount(){
        int fileCount = 0;
        File dir = new File("/storage/emulated/0/OneMob");
        File[] files = dir.listFiles();
        fileCount = files.length;
        return fileCount;
    }

    public String[] getFileName(){
        File dir = new File("/storage/emulated/0/OneMob");
        File[] files = dir.listFiles();
        String[] filesName = new String[files.length];
        for (int i = 0 ; i < files.length ; i++){
            filesName[i] = files[i].getName();
        }
        return filesName;
    }

    private ArrayList<Video> genVideos(int fileCount, String[] videosName) {
        ArrayList<Video> videos = new ArrayList<Video>();
        Video[] arrayVideo = new Video[fileCount];
        for (int k = 0 ; k < arrayVideo.length ; k++){
            arrayVideo[k] = new Video("link", videosName[k]);
        }
        for (int i = 0 ; i < fileCount ; i++){
            videos.add(arrayVideo[i]);
        }
        return videos;
    }
}
