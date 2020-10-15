package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import com.example.myapplication.JsonPackage.JsonPostRegistration;
import com.example.myapplication.ui.notifications.NotificationsFragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

public class MainActivity extends AppCompatActivity {

    String token;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        BottomNavigationView navView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        try {
            try {
                String intentString = getIntent().getExtras().getString("token");
                token = intentString;
            } catch (NullPointerException e){
                e.printStackTrace();
                Log.e("NullPointerException!", e.getMessage());
            }
            Intent intent  = new Intent(MainActivity.this, LoginActivity.class);
            intent.putExtra("tokenLogin", token);
            NotificationsFragment notificationsFragment = new NotificationsFragment();
            Bundle bundle = new Bundle();
            bundle.putString("token", token);
            notificationsFragment.setArguments(bundle);
            getSupportFragmentManager().beginTransaction().add(R.id.nav_host_fragment, notificationsFragment).commit();
        } catch (Exception e){
            e.printStackTrace();
            Log.e("Whole Exception!", e.getMessage());
        }
        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(R.id.navigation_videos, R.id.navigation_exams, R.id.navigation_moreOptions).build();
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);
    }
}
