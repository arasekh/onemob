package com.example.myapplication;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.media.MediaMetadataRetriever;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.widget.MediaController;
import android.widget.VideoView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okio.BufferedSink;
import okio.Okio;

public class ShowVideoActivity extends AppCompatActivity {

    VideoView videoViewShow;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_video);
        try {
            videoViewShow = findViewById(R.id.videoViewShow);
            String token = getIntent().getExtras().getString("tokenShowVideo");
            String videoTitle = getIntent().getExtras().getString("VideoTitleList");
            ShowVideoAsyncTask showVideoAsyncTask = (ShowVideoAsyncTask) new ShowVideoAsyncTask(token,videoTitle, videoViewShow, ShowVideoActivity.this).execute();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    //Get video's path from VideosFragment class and show video in a VideoView.
    public void showVideo(String key, VideoView videoViewShow){
        String path = getIntent().getStringExtra(key);
        videoViewShow.setVideoPath(path);
        videoViewShow.start();
        MediaController controller = new MediaController(this);
        controller.setAnchorView(videoViewShow);
        videoViewShow.setMediaController(controller);
    }

    public void secondShowVideo(File file, VideoView videoViewShow, Context context){
        videoViewShow.setVideoPath(file.getPath());
        videoViewShow.start();
        MediaController controller = new MediaController(context);
        controller.setAnchorView(videoViewShow);
        videoViewShow.setMediaController(controller);
    }
}

class ShowVideoAsyncTask extends AsyncTask{

    String videoTitle = "video";
    String fileName = "VID_20970721_113800_342.mp4";
    String token = "";
    Response response = null;
    VideoView videoView = null;
    Context context = null;
    File file = null;
    File root;
    FileOutputStream fileOutputStream;
    String path;

    public ShowVideoAsyncTask(String token,String videoTitle, VideoView videoView, Context context) {
        this.token = token;
        this.videoTitle = videoTitle;
        this.videoView = videoView;
        this.context = context;
    }

    @Override
    protected Object doInBackground(Object[] objects) {
        try {
            OkHttpClient client = new OkHttpClient.Builder().build();
            Request request = new Request.Builder().url("http://138.201.6.240:8000/api/video/"+videoTitle).method("GET", null).addHeader("Authorization", "Token "+token).build();
            response = null;
            try {
//                path = "/storage/emulated/0/OneMob";
                path = context.getExternalFilesDir(null).getAbsolutePath();
                file = new File(path);
                if (!file.exists()){
                    file.mkdirs();
                    Log.d("FILE EXISTS", file.getAbsolutePath());
                }
                root = new File(file, fileName);
                response = client.newCall(request).execute();
                fileOutputStream = new FileOutputStream(root);
                fileOutputStream.write(response.body().bytes());
                fileOutputStream.close();
                response.body().close();
                File[] listOne = file.listFiles();
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

    @Override
    protected void onPostExecute(Object o) {
        super.onPostExecute(o);
        try {
            File fileSecond = new File(path+"/"+fileName);
            Log.d("file", file.getAbsolutePath());
//            Log.d("fileOutputStream", fileOutputStream.toString());
            videoView.setVideoPath(fileSecond.getAbsolutePath());
            videoView.start();
            MediaController controller = new MediaController(context);
            controller.setAnchorView(videoView);
            videoView.setMediaController(controller);
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}