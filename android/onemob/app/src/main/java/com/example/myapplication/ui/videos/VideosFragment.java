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

import com.example.myapplication.JsonPackage.JsonVideoList;
import com.example.myapplication.JsonPackage.JsonVideosDownload;
import com.example.myapplication.MainActivity;
import com.example.myapplication.R;
import com.example.myapplication.ShowVideoActivity;
import com.example.myapplication.UtilToken;
import com.example.myapplication.Video;
import com.example.myapplication.VideoListAdapter;

import java.io.File;
import java.lang.reflect.Array;
import java.util.ArrayList;

public class VideosFragment extends Fragment {

    private VideosViewModel videosViewModel;
    String videoUrl = "link";
    String[] videosName;
    ListView videoListView;
    String token = "token";

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        videosViewModel = ViewModelProviders.of(this).get(VideosViewModel.class);
        View root = inflater.inflate(R.layout.fragment_videos, container, false);
        ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.READ_EXTERNAL_STORAGE,Manifest.permission.WRITE_EXTERNAL_STORAGE},111);

        videoListView = (ListView) root.findViewById(R.id.videosListView);

        String path = "/storage/emulated/0/OneMob";
        File file = new File(path);
        if (!file.exists()){
            file.mkdirs();
            Log.d("FILE EXISTS", file.getAbsolutePath());
        }

        try {
            token = UtilToken.token;
            Log.d("tokenFromArg", token);
        } catch (NullPointerException e){
            e.printStackTrace();
        }

        JsonVideosDownload jsonVideosDownload = (JsonVideosDownload) new JsonVideosDownload(token).execute();
        JsonVideoList jsonVideoList = (JsonVideoList) new JsonVideoList(token, getContext(), getActivity(), videoListView).execute();

        return root;
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

                } else {
                    Toast.makeText(getContext(), "Permission denied...!", Toast.LENGTH_LONG).show();
                }
            }
        }
    }
}