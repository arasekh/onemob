package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.media.MediaMetadataRetriever;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.widget.MediaController;
import android.widget.VideoView;

import java.io.File;

public class ShowVideoActivity extends AppCompatActivity {

    VideoView videoViewShow;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_video);

        videoViewShow = findViewById(R.id.videoViewShow);
        showVideo("VideoPath",videoViewShow);
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
}