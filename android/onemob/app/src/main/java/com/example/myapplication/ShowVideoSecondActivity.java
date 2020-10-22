package com.example.myapplication;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.widget.MediaController;
import android.widget.VideoView;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class ShowVideoSecondActivity extends AppCompatActivity {

    VideoView videoView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_video_second);
        videoView = findViewById(R.id.secondVideoView);
        String token = getIntent().getExtras().getString("tokenShowVideo");
        ShowVideoSecondAsync showVideoSecondAsync = (ShowVideoSecondAsync) new ShowVideoSecondAsync(token, videoView, ShowVideoSecondActivity.this).execute();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
}

class ShowVideoSecondAsync extends AsyncTask{

    String videoTitle = "video2";
    String fileName = "01_Retrofit.mp4";
    String token = "";
    Response response = null;
    VideoView videoView = null;
    Context context = null;
    File dir;
    FileOutputStream fileOutputStream;

    public ShowVideoSecondAsync(String token, VideoView videoView, Context context) {
        this.token = token;
        this.videoView = videoView;
        this.context = context;
    }

    @Override
    protected Object doInBackground(Object[] objects) {
        dir = new File("/storage/emulated/0/", "OneMob");
        if (!dir.exists()){
            dir.mkdirs();
        }
        OkHttpClient client = new OkHttpClient.Builder().build();
        Request request = new Request.Builder().url("http://192.168.1.5:8000/api/video/"+videoTitle).method("GET", null).addHeader("Authorization", "Token "+token).build();
        try {
            response = client.newCall(request).execute();
            fileOutputStream = new FileOutputStream(Environment.getExternalStorageDirectory().getAbsolutePath()+"/Download/"+fileName);
            fileOutputStream.write(response.body().bytes());
            fileOutputStream.close();
            response.body().close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(Object o) {
        super.onPostExecute(o);
        File file = new File(Environment.getExternalStorageDirectory().getAbsolutePath()+"/Download/"+fileName);
        Log.d("file", file.getAbsolutePath());
        Log.d("fileOutputStream", fileOutputStream.toString());
        videoView.setVideoPath(file.getAbsolutePath());
        videoView.start();
        MediaController controller = new MediaController(context);
        controller.setAnchorView(videoView);
        videoView.setMediaController(controller);
    }

    public void readVideoFromFile() {
        File dir = Environment.getExternalStoragePublicDirectory(this.dir.getAbsolutePath());
        File[] files = dir.listFiles();
        int fileCount = getFileCount();
        videoView.setVideoPath(files[fileCount-1].getAbsolutePath());
        videoView.start();
        MediaController controller = new MediaController(context);
        controller.setAnchorView(videoView);
        videoView.setMediaController(controller);
//        Intent intent = new Intent(getContext(), ShowVideoActivity.class);
//        intent.putExtra("VideoPath",files[position].getAbsolutePath());
//        startActivity(intent);
    }

    public int getFileCount(){
        int fileCount = 0;
        File dir = Environment.getExternalStoragePublicDirectory(this.dir.getAbsolutePath());
        File[] files = dir.listFiles();
        fileCount = files.length;
        return fileCount;
    }
}