package com.example.myapplication;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceControl;

import com.example.myapplication.JsonPackage.JsonPostRegistration;
import com.example.myapplication.JsonPackage.JsonVideoList;
import com.example.myapplication.JsonPackage.JsonVideosDownload;
import com.example.myapplication.ui.notifications.NotificationsFragment;
import com.example.myapplication.ui.videos.VideosFragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.FragmentActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    String token;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        BottomNavigationView navView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.READ_EXTERNAL_STORAGE,Manifest.permission.WRITE_EXTERNAL_STORAGE},111);
        try {
            try {
                token = UtilToken.token;
                Log.d("tokenUtil", token);
                Intent intent  = new Intent(MainActivity.this, LoginActivity.class);
                intent.putExtra("tokenLogin", token);
            } catch (NullPointerException e){
                e.printStackTrace();
                Log.e("NullPointerException!", e.getMessage());
            }

        } catch (Exception e){
            e.printStackTrace();
            Log.e("Whole Exception!", e.getMessage());
        }
        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(R.id.navigation_videos, R.id.navigation_exams, R.id.navigation_moreOptions).build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
}

