package com.example.myapplication;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.List;

public class QuizResultListAdapter extends ArrayAdapter<QuizResult> {

    private static final String TAG = "QuizResultAdapter";
    private Context quizResultContext;
    int quizResultResource;

    public QuizResultListAdapter(@NonNull Context context, int resource, @NonNull List<QuizResult> objects) {
        super(context, resource, objects);
        quizResultContext = context;
        quizResultResource = resource;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        String yourSelectedSwitch = getItem(position).getYourSelectedSwitch();
        String trueSwitch = getItem(position).getTrueSwitch();

        QuizResult quizResult = new QuizResult(yourSelectedSwitch, trueSwitch);

        LayoutInflater layoutInflater = LayoutInflater.from(quizResultContext);
        convertView = layoutInflater.inflate(quizResultResource, parent, false);

        TextView lblYourSelectedSwitch = convertView.findViewById(R.id.lblYourSelectedSwitch);
        lblYourSelectedSwitch.setText(yourSelectedSwitch);
        TextView lblTrueSwitch = convertView.findViewById(R.id.lblTrueSwitch);
        lblTrueSwitch.setText(trueSwitch);

        return convertView;
    }
}
