package com.example.myapplication.JsonPackage;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;
import android.widget.TextView;

import androidx.fragment.app.FragmentActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import com.example.myapplication.LoginActivity;
import com.example.myapplication.MainActivity;
import com.example.myapplication.R;
import com.example.myapplication.UtilToken;
import com.example.myapplication.ui.notifications.NotificationsFragment;
import com.example.myapplication.ui.videos.VideosFragment;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Credentials;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

//This class for sending the username and password to the server to for logging in.
public class JsonPostLogin extends AsyncTask {
    public static final MediaType jsonMediaType = MediaType.parse("application/json; charset=utf-8");

    String username = "";
    String password = "";

    String httpCode;

    String tokenLogin = "0";

    Activity activity = null;

    EditText editTextUserName;
    EditText editTextPassword;
    TextView lblLoginStatus;

    public JsonPostLogin(String username, String password, Activity activity, EditText editTextUserName, EditText editTextPassword, TextView lblLoginStatus) {
        this.username = username;
        this.password = password;
        this.activity = activity;
        this.editTextUserName = editTextUserName;
        this.editTextPassword = editTextPassword;
        this.lblLoginStatus = lblLoginStatus;
    }

    public JsonPostLogin() { }

    public JsonPostLogin(Activity activity ,String username, String password) {
        this.activity = activity;
        this.username = username;
        this.password = password;
    }

    public String getToken() {
        return tokenLogin;
    }

    @Override
    protected Object doInBackground(Object[] objects) {
        try {
            JSONObject jsonObject = new JSONObject();
            try {
                jsonObject.put("username",username);
                jsonObject.put("password",password);
            } catch (JSONException e) {
                e.printStackTrace();
                Log.e("JsonObject Error!", e.getMessage());
            }
            OkHttpClient okHttpClient = new OkHttpClient();
            String adminInfo = Credentials.basic("Alineo","145");
            RequestBody requestBody = RequestBody.create(jsonMediaType, jsonObject.toString());
            Request request = new Request.Builder().url("http://192.168.1.5:8000/api/login/").post(requestBody).addHeader("Authorization",adminInfo).build();
            Response response = null;
            String result = "";
            JSONObject jsonObjectToken = null;
            try {
                response = okHttpClient.newCall(request).execute();
                httpCode = String.valueOf(response.code());
                Log.d("httpCode", httpCode);
                result = response.body().string();
                jsonObjectToken = new JSONObject(result);
                tokenLogin = jsonObjectToken.getString("token");
            } catch (IOException e) {
                e.printStackTrace();
                tokenLogin = "0";
                Log.e("error",e.getMessage());
            } catch (NullPointerException e){
                e.printStackTrace();
                tokenLogin = "0";
                Log.e("error",e.getMessage());
            }
            Log.d("Login Json!", result);
            Log.d("Token JsonPostLogin!", tokenLogin);
        } catch (Exception e){
            e.printStackTrace();
            Log.e("Whole Exception!", e.getMessage());
        }
        return null;
    }

    @Override
    protected void onPostExecute(Object o) {
        super.onPostExecute(o);
        try {
            if (httpCode.equals("200")){
                UtilToken.token = tokenLogin;
                Intent intentToMain = new Intent(activity, MainActivity.class);
                activity.startActivity(intentToMain);
            } else if (httpCode.equals("400") || httpCode.equals("404")){
                editTextUserName.setText("");
                editTextPassword.setText("");
                editTextUserName.setError("لطفا نام کاربری معتبر وارد کنید!");
                editTextPassword.setError("لطفا رمز عبور معتبر وارد کنید!");
                lblLoginStatus.setTextColor(Color.RED);
                lblLoginStatus.setText("نام کاربری یا رمز عبور معتبر نمی باشد!");
            }
        } catch (Exception e){
            e.printStackTrace();
        }

    }
}
