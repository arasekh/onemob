package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

public class ShowQuizResultActivity extends AppCompatActivity {

    TextView lblShowScore;

    String score = "";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_quiz_result);

        lblShowScore = findViewById(R.id.lblShowScore);

        score = getIntent().getExtras().getString("score");
        lblShowScore.setText(score);

    }
}