package com.example.myapplication.JsonPackage;

import android.app.Activity;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.ListView;
import android.widget.VideoView;

import com.example.myapplication.Video;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;

import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Request.Builder;
import okhttp3.Response;

public class JsonVideosDownload extends AsyncTask {

    ArrayList<JSONObject> videosJsonObjectArrayList = new ArrayList<>();
    String[] videosName = null;
    String[] videosTitle = null;
    String token;
    Activity activity = null;
    Context context = null;
    ListView videosListView;
    String path;
    File file;

    String videoTitle = "video";
    String fileName = "VID_20970721_113800_342.mp4";
    String tokenVideoDownload = "";
    Response responseVideoDownload = null;
    VideoView videoView = null;
//    Context context = null;
    File fileVideoDownload = null;
    File root;
    FileOutputStream fileOutputStream;
    String pathVideoDownload;

    public JsonVideosDownload(String token, String videoTitle) {
        this.token = token;
        this.videoTitle = videoTitle;
    }

    public JsonVideosDownload(String token) {
        this.token = token;
    }

    public JsonVideosDownload(String token, Context context) {
        this.token = token;
        this.context = context;
    }

    @Override
    protected Object doInBackground(Object[] objects) {
        try {
            OkHttpClient clientVideoDownload = new OkHttpClient.Builder().build();
            Request requestVideoDownload = new Request.Builder().url("http://192.168.1.5:8000/api/video/"+videoTitle).method("GET", null).addHeader("Authorization", "Token "+token).build();
            responseVideoDownload = null;
            try {
                pathVideoDownload = "/storage/emulated/0/OneMob";
                fileVideoDownload = new File(pathVideoDownload);
                if (!fileVideoDownload.exists()){
                    fileVideoDownload.mkdirs();
                    Log.d("FILE EXISTS", fileVideoDownload.getAbsolutePath());
                }
                root = new File(fileVideoDownload, fileName);
                responseVideoDownload = clientVideoDownload.newCall(requestVideoDownload).execute();
                fileOutputStream = new FileOutputStream(root);
                fileOutputStream.write(responseVideoDownload.body().bytes());
                fileOutputStream.close();
                responseVideoDownload.body().close();
                File[] listOne = fileVideoDownload.listFiles();
                for (int i = 0 ; i < listOne.length ; i++){
                    Log.d("listOne", listOne[i].getAbsolutePath());
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (Exception e){
            e.printStackTrace();
        }
        return null;
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
