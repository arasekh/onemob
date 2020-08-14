package com.example.myapplication;

import android.content.Intent;
import android.os.Bundle;
import android.telephony.mbms.StreamingServiceInfo;
import android.text.method.LinkMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

/**
 * Created by tutlane on 08-01-2018.
 */

public class RegistrationActivity extends AppCompatActivity {

    EditText txtFullName;
    EditText txtEmailAddress;
    EditText txtPassword;
    Button btnSignUp;
    TextView lblHaveAnAccount;

    String fullName;
    String emailAddress;
    String password;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.registration_activity);
        TextView login = (TextView)findViewById(R.id.lblSignUpPage);
        if (LinkMovementMethod.getInstance() != null){
            login.setMovementMethod(LinkMovementMethod.getInstance());
        }
        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(RegistrationActivity.this, LoginActivity.class);
                startActivity(intent);
            }
        });

        txtFullName = findViewById(R.id.txtName);
        txtEmailAddress = findViewById(R.id.txtEmailAddress);
        txtPassword = findViewById(R.id.txtPassword);
        btnSignUp = findViewById(R.id.btnSignUp);
        lblHaveAnAccount = findViewById(R.id.lblHaveAnAccount);

        lblHaveAnAccount.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(RegistrationActivity.this, LoginActivity.class);
                startActivity(intent);}
        });

        btnSignUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                fullName = txtFullName.getText().toString();
                emailAddress = txtEmailAddress.getText().toString();
                password = txtPassword.getText().toString();
            }
        });
    }
}