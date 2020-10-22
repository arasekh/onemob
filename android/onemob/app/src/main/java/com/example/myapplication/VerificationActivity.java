package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.example.myapplication.JsonPackage.JsonConfirmEmail;

public class VerificationActivity extends AppCompatActivity {

EditText editTextConfirmEmailNotification;
Button btnConfirmEmailNotification;
TextView lblConfirmStatus;

String confirmEmailCode;
String token;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_verification);
        try {
            setUI();
            setListener();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    private void setUI(){
        editTextConfirmEmailNotification = findViewById(R.id.editTextConfirmEmailNotification);
        btnConfirmEmailNotification = findViewById(R.id.btnConfirmEmailNotification);
        lblConfirmStatus = findViewById(R.id.lblConfirmStatus);
    }

    private void setListener(){
        btnConfirmEmailNotification.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                confirmEmailCode = editTextConfirmEmailNotification.getText().toString();
                try {
                    token = UtilToken.token;
                } catch (NullPointerException e){
                    e.printStackTrace();
                    token = "The token was null.";
                }
                JsonConfirmEmail jsonConfirmEmail = (JsonConfirmEmail) new JsonConfirmEmail(token, confirmEmailCode, editTextConfirmEmailNotification, lblConfirmStatus, VerificationActivity.this).execute();
            }
        });
    }
}