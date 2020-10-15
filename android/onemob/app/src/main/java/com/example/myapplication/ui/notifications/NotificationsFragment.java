package com.example.myapplication.ui.notifications;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.example.myapplication.JsonPackage.JsonConfirmEmail;
import com.example.myapplication.JsonPackage.JsonPostLogin;
import com.example.myapplication.MainActivity;
import com.example.myapplication.R;

public class NotificationsFragment extends Fragment {

    private NotificationsViewModel notificationsViewModel;

    EditText editTextFirstNameNotification;
    EditText editTextLastNameNotification;
    EditText editTextUserNameNotification;
    EditText editTextEmailNotification;
    EditText editTextConfirmEmailNotification;
    TextView lblConfirmStatus;
    Button btnConfirmEmail;

    String confirmEmailCode;
    String token = "";

    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        notificationsViewModel = ViewModelProviders.of(this).get(NotificationsViewModel.class);
        View root = inflater.inflate(R.layout.fragment_notifications, container, false);
        final TextView textView = root.findViewById(R.id.text_notifications);
        notificationsViewModel.getText().observe(this, new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });

        try {
            setupUI(root);
            setupListeners();
        } catch (Exception e){
            e.printStackTrace();
            Log.e("Whole Exception!", e.getMessage());
        }
        return root;
    }

    private void setupUI(View root){
        editTextFirstNameNotification = root.findViewById(R.id.editTextFirstNameNotification);
        editTextLastNameNotification = root.findViewById(R.id.editTextLastNameNotification);
        editTextUserNameNotification = root.findViewById(R.id.editTextUserNameNotification);
        editTextEmailNotification = root.findViewById(R.id.editTextEmailNotification);
        editTextConfirmEmailNotification = root.findViewById(R.id.editTextConfirmEmailNotification);
        lblConfirmStatus = root.findViewById(R.id.lblConfirmStatus);
        btnConfirmEmail = root.findViewById(R.id.btnConfirmEmailNotification);
    }

    private void setupListeners(){
        btnConfirmEmail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                confirmEmailCode = editTextConfirmEmailNotification.getText().toString();
                try {
                    token = getArguments().getString("token","");
                } catch (NullPointerException e){
                    e.printStackTrace();
                    token = "The token was null.";
                }
                Log.d("token Notification", token);
                JsonConfirmEmail jsonConfirmEmail = (JsonConfirmEmail) new JsonConfirmEmail(token, confirmEmailCode, editTextConfirmEmailNotification, lblConfirmStatus).execute();
//                if (token.equals("The token was null.")){
//                    lblConfirmStatus.setText("تائید ایمیل ناموفق بود!");
//                } else {
//                    lblConfirmStatus.setText("تائید ایمیل موفقیت آمیز بود!");
//                }
            }
        });
    }
}