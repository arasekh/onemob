package com.example.myapplication;

import android.content.Context;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.example.myapplication.JsonPackage.JsonShowQuiz;
import com.example.myapplication.JsonPackage.JsonSubmitQuiz;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class ShowExamActivity extends AppCompatActivity {

    EditText editTextQuestion;
    RadioGroup radioGroup;
    RadioButton radioButtonFirst;
    RadioButton radioButtonSecond;
    RadioButton radioButtonThird;
    RadioButton radioButtonForth;
    Button btnNext;
    Button btnPrevious;
    Button btnSubmit;
    String[] quizTitles = null;
    String title;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_exam);
        try {
            setupUI();
            radioButtonFirst = findViewById(R.id.radioButtonFirst);
            radioButtonSecond = findViewById(R.id.radioButtonSecond);
            radioButtonThird = findViewById(R.id.radioButtonThird);
            radioButtonForth = findViewById(R.id.radioButtonForth);

//        quizTitles = new String[1];
//        quizTitles = getIntent().getStringArrayExtra("titlesArray");
            title = getIntent().getStringExtra("titlesArray");
            JsonShowQuizInActivity jsonShowQuizInActivity1 = (JsonShowQuizInActivity) new JsonShowQuizInActivity(title, UtilToken.token, ShowExamActivity.this, btnNext, btnPrevious, btnSubmit, editTextQuestion, radioGroup, radioButtonFirst, radioButtonSecond, radioButtonThird, radioButtonForth).execute();

//        JsonShowQuizInActivity jsonShowQuizInActivity = (JsonShowQuizInActivity) new JsonShowQuizInActivity(title, UtilToken.token, btnNext, btnPrevious, editTextQuestion, radioButtonFirst, radioButtonSecond, radioButtonThird, radioButtonForth).execute();
            btnNext.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    int selectedRadio = radioGroup.getCheckedRadioButtonId();
                    radioButtonFirst = findViewById(selectedRadio);
                    Toast.makeText(ShowExamActivity.this, radioButtonFirst.getText(), Toast.LENGTH_LONG).show();
                }
            });
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    private void setupUI(){
        editTextQuestion = findViewById(R.id.editTextQuestion);
        radioGroup = findViewById(R.id.radioGroup);
        btnNext = findViewById(R.id.btnNext);
        btnPrevious = findViewById(R.id.btnPrevious);
        btnSubmit = findViewById(R.id.btnSubmit);
    }
}

class JsonShowQuizInActivity extends AsyncTask {

    int questionsCounter;

    ArrayList<JSONObject> questionsJsonObjectArray = new ArrayList<>();
    ArrayList<JSONObject> question = new ArrayList<>();
    ArrayList<String> questionsTextArray = new ArrayList<>();
    ArrayList<String> questionsIdArray = new ArrayList<>();
    ArrayList<JSONArray> answers = new ArrayList<>();
    JSONObject[][] eachAnswer = null;
    String[][] answersText = null;
    String[][] answersId = null;
    ArrayList<String> selectedAnswersId = new ArrayList<>();
    int[] examsId = null;
    String[] questionsText = null;
    String quizTitle = "";
    String token = "";

    Context context;
    Button btnNext;
    Button btnPrevious;
    Button btnSubmit;
    EditText editTextQuestion;
    RadioGroup radioGroup;
    RadioButton radioButtonFirst;
    RadioButton radioButtonSecond;
    RadioButton radioButtonThird;
    RadioButton radioButtonForth;

    public JsonShowQuizInActivity(String quizTitle, String token, Context context, Button btnNext, Button btnPrevious, Button btnSubmit, EditText editTextQuestion, RadioGroup radioGroup, RadioButton radioButtonFirst, RadioButton radioButtonSecond, RadioButton radioButtonThird, RadioButton radioButtonForth) {
        this.quizTitle = quizTitle;
        this.token = token;
        this.context = context;
        this.btnNext = btnNext;
        this.btnPrevious = btnPrevious;
        this.btnSubmit = btnSubmit;
        this.editTextQuestion = editTextQuestion;
        this.radioGroup = radioGroup;
        this.radioButtonFirst = radioButtonFirst;
        this.radioButtonSecond = radioButtonSecond;
        this.radioButtonThird = radioButtonThird;
        this.radioButtonForth = radioButtonForth;
    }

    public JsonShowQuizInActivity(String quizTitle, String token) {
        this.quizTitle = quizTitle;
        this.token = token;
    }

    public JsonShowQuizInActivity(String quizTitle, String token, EditText editTextQuestion) {
        this.quizTitle = quizTitle;
        this.token = token;
        this.editTextQuestion = editTextQuestion;
    }

    @Override
    protected Object doInBackground(Object[] objects) {
        try {
            OkHttpClient okHttpClient = new OkHttpClient.Builder().build();
            Request request = new Request.Builder().url("http://138.201.6.240:8000/api/get-quiz/"+quizTitle).method("GET", null).addHeader("Authorization", "Token "+token).build();
            Response response = null;
            String resultShowExam = "";
            JSONObject jsonObject = null;
            JSONArray jsonArray = null;
            JSONArray jsonArrayQuestion = null;
            try {
                response = okHttpClient.newCall(request).execute();
                resultShowExam = response.body().string();
                jsonObject = new JSONObject(resultShowExam);
                jsonArray = jsonObject.getJSONArray("quiz");

                eachAnswer = new JSONObject[jsonArray.length()][4];
                answersText = new String[jsonArray.length()][4];
                answersId = new String[jsonArray.length()][4];
                for (int i = 0 ; i < jsonArray.length() ; i++){
                    questionsJsonObjectArray.add(jsonArray.getJSONObject(i));
                    question.add(questionsJsonObjectArray.get(i).getJSONObject("question"));
                    questionsTextArray.add(question.get(i).getString("text"));
                    questionsIdArray.add(question.get(i).getString("id"));
                    answers.add(questionsJsonObjectArray.get(i).getJSONArray("answers"));
                    for (int j = 0 ; j < 4 ; j++){
                        eachAnswer[i][j] = answers.get(i).getJSONObject(j);
                        answersText[i][j] = eachAnswer[i][j].getString("text");
                        answersId[i][j] = eachAnswer[i][j].getString("id");
                    }
                }
            } catch (IOException | NullPointerException e){
                e.printStackTrace();
            }
            Log.d("resultShowExam", resultShowExam);
            Log.d("quiz_array", String.valueOf(jsonArray));
            for (int i = 0 ; i < jsonArray.length() ; i++){
                Log.d("question", String.valueOf(questionsJsonObjectArray.get(i)));
                Log.d("question-rrrr", String.valueOf(question.get(i)));
                Log.d("questions-text", String.valueOf(questionsTextArray.get(i)));
                Log.d("questions-id", String.valueOf(questionsIdArray.get(i)));
                Log.d("answers", String.valueOf(answers.get(i)));
                for (int j = 0 ; j < 4 ; j++){
                    Log.d("eachAnswers", String.valueOf(eachAnswer[i][j]));
                    Log.d("answers-text", String.valueOf(answersText[i][j]));
                    Log.d("answers-id", String.valueOf(answersId[i][j]));
                }
            }
        } catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }

    @Override
    protected void onPostExecute(Object o) {
        super.onPostExecute(o);

        try {
            editTextQuestion.setText(questionsTextArray.get(0));
            radioButtonFirst.setText(answersText[0][0]);
            radioButtonSecond.setText(answersText[0][1]);
            radioButtonThird.setText(answersText[0][2]);
            radioButtonForth.setText(answersText[0][3]);
            questionsCounter = 0;
            btnNext.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    radioGroup.clearCheck();
                    int selected = radioGroup.getCheckedRadioButtonId();
                    if (selected == R.id.radioButtonFirst){
                        selectedAnswersId.add(answersId[questionsCounter][0]);
                    } else if (selected == R.id.radioButtonSecond){
                        selectedAnswersId.add(answersId[questionsCounter][1]);
                    } else if (selected == R.id.radioButtonThird){
                        selectedAnswersId.add(answersId[questionsCounter][2]);
                    } else if (selected == R.id.radioButtonForth){
                        selectedAnswersId.add(answersId[questionsCounter][3]);
                    } else {
                        Toast.makeText(context, "لطفا گزینه ای را انتخاب نمایید!", Toast.LENGTH_LONG).show();
                    }

                    if (questionsCounter < questionsTextArray.size()){
                        if (questionsCounter < questionsTextArray.size() -1){
                            questionsCounter++;
                        }
                        editTextQuestion.setText(questionsTextArray.get(questionsCounter));
                        radioButtonFirst.setText(answersText[questionsCounter][0]);
                        radioButtonSecond.setText(answersText[questionsCounter][1]);
                        radioButtonThird.setText(answersText[questionsCounter][2]);
                        radioButtonForth.setText(answersText[questionsCounter][3]);
                    } else {
                        questionsCounter = questionsTextArray.size() - 1;
                    }
                    if (questionsCounter >= 0 && questionsCounter < questionsTextArray.size()-1){
                        btnSubmit.setText(questionsCounter+"/"+questionsTextArray.size());
                    } else if (questionsCounter == questionsTextArray.size()-1){
                        btnSubmit.setText("پایان آزمون");
                        btnSubmit.setOnClickListener(new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                JsonSubmitQuiz jsonSubmitQuiz = (JsonSubmitQuiz) new JsonSubmitQuiz(UtilToken.token, questionsIdArray, selectedAnswersId, context).execute();
                            }
                        });
                    }
                }
            });
            btnPrevious.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    radioGroup.clearCheck();
                    if (questionsCounter > 0){
                        questionsCounter--;
                        editTextQuestion.setText(questionsTextArray.get(questionsCounter));
                        radioButtonFirst.setText(answersText[questionsCounter][0]);
                        radioButtonSecond.setText(answersText[questionsCounter][1]);
                        radioButtonThird.setText(answersText[questionsCounter][2]);
                        radioButtonForth.setText(answersText[questionsCounter][3]);
                    } else {
                        questionsCounter = 0;
                    }
                    if (questionsCounter >= 0 && questionsCounter < questionsTextArray.size()-1){
                        btnSubmit.setText((questionsCounter+1)+"/"+questionsTextArray.size());
                    } else if (questionsCounter == questionsTextArray.size()-1){
                        btnSubmit.setText("پایان آزمون");
                        btnSubmit.setOnClickListener(new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                JsonSubmitQuiz jsonSubmitQuiz = (JsonSubmitQuiz) new JsonSubmitQuiz(UtilToken.token, questionsIdArray, selectedAnswersId, context).execute();
                            }
                        });
                    }
                }
            });
            if (questionsCounter >= 0 && questionsCounter < questionsTextArray.size()-1){
                btnSubmit.setText((questionsCounter+1)+"/"+questionsTextArray.size());
            } else if (questionsCounter == questionsTextArray.size()-1){
                btnSubmit.setText("پایان آزمون");
                btnSubmit.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        JsonSubmitQuiz jsonSubmitQuiz = (JsonSubmitQuiz) new JsonSubmitQuiz(UtilToken.token, questionsIdArray, selectedAnswersId, context).execute();
                    }
                });
            }
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
