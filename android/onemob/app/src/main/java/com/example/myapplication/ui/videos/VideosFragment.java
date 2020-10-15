package com.example.myapplication.ui.videos;

import android.Manifest;
import android.app.DownloadManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.example.myapplication.MainActivity;
import com.example.myapplication.R;
import com.example.myapplication.ShowVideoActivity;
import com.example.myapplication.Video;
import com.example.myapplication.VideoListAdapter;

import java.io.File;
import java.lang.reflect.Array;
import java.util.ArrayList;

public class VideosFragment<pee> extends Fragment {

    private VideosViewModel videosViewModel;
    String videoUrl = "link";

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        videosViewModel = ViewModelProviders.of(this).get(VideosViewModel.class);
        View root = inflater.inflate(R.layout.fragment_videos, container, false);
//        final TextView textView = root.findViewById(R.id.text_videos);
//        videosViewModel.getText().observe(this, new Observer<String>() {
//            @Override
//            public void onChanged(@Nullable String s) {
//                textView.setText(s);
//            }
//        });

        final ListView videoListView = (ListView) root.findViewById(R.id.videosListView);
        int fileCount = getFileCount();
        Log.d("fileCount", String.valueOf(fileCount));
        String[] filesName = getFileName();
        for (int i = 0 ; i < filesName.length ; i++){
            Log.d("fileName", filesName[i]);
        }
        ArrayList<Video> videosList = genVideos(fileCount);
        VideoListAdapter adapter = new VideoListAdapter(this.getActivity(), R.layout.videos_view_layout, videosList);
        videoListView.setAdapter(adapter);
        videoListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M){
                    if (ActivityCompat.checkSelfPermission(getContext(), Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED){
                        String[] permissions = {Manifest.permission.WRITE_EXTERNAL_STORAGE};
                        requestPermissions(permissions, 1000);
                    } else {
//                        startDownloading("https://9429db549a83.ngrok.io/api/video/a");
                        readVideoFromFile(i);
                    }
                } else {
//                    startDownloading("https://9429db549a83.ngrok.io/api/video/a");
                    readVideoFromFile(i);
                }
            }
        });
        return root;
    }



    private ArrayList<Video> genVideos(int fileCount) {
        ArrayList<Video> videos = new ArrayList<Video>();
        Video[] arrayVideo = new Video[fileCount];
        String[] videosName = getFileName();
        for (int k = 0 ; k < arrayVideo.length ; k++){
            arrayVideo[k] = new Video("link", videosName[k]);
        }
//        for (int j = 0 ; j < arrayVideo.length ; j++){
//            arrayVideo[j].setVideoName(videosName[j]);
//        }
        for (int i = 0 ; i < fileCount ; i++){
            videos.add(arrayVideo[i]);
        }
//        Video v1 = new Video("link","ویدیو یک");
//        videos.add(v1);
//        Video v2 = new Video("link","ویدیو دو");
//        videos.add(v2);
//        Video v3 = new Video("link","ویدیو سه");
//        videos.add(v3);
//        Video v4 = new Video("link","ویدیو چهار");
//        videos.add(v4);
//        Video v5 = new Video("link","ویدیو پنج");
//        videos.add(v5);
        return videos;
    }

    //Read files from Download folder in device and send files to the ShowVideoActivity class to show videos.
    public void readVideoFromFile(int position) {
        File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
        File[] files = dir.listFiles();
        Intent intent = new Intent(getContext(), ShowVideoActivity.class);
        intent.putExtra("VideoPath",files[position].getAbsolutePath());
        startActivity(intent);
    }

    public int getFileCount(){
        int fileCount = 0;
        File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
        File[] files = dir.listFiles();
        fileCount = files.length;
        return fileCount;
    }

    public String[] getFileName(){
        File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
        File[] files = dir.listFiles();
        String[] filesName = new String[files.length];
        for (int i = 0 ; i < files.length ; i++){
            filesName[i] = files[i].getName();
        }
        return filesName;
    }

    //Download video with URL and show this progress in the notification and after downloading , push videos into the Download folder in device.
    public void startDownloading(String url){
        DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
        request.setAllowedNetworkTypes(DownloadManager.Request.NETWORK_WIFI | DownloadManager.Request.NETWORK_MOBILE);
        request.setTitle("Video");
        request.setDescription("Video Downloading!");
        request.allowScanningByMediaScanner();
        request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
        request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS , ""+System.currentTimeMillis());
        DownloadManager downloadManager = (DownloadManager) getActivity().getBaseContext().getSystemService(Context.DOWNLOAD_SERVICE);
        downloadManager.enqueue(request);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch (requestCode){
            case 1000:{
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED){
                    startDownloading("https://9429db549a83.ngrok.io/api/video/a");
                } else {
                    Toast.makeText(getContext(), "Permission denied...!", Toast.LENGTH_LONG).show();
                }
            }
        }
    }
}