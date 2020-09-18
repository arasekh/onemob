package com.example.myapplication.ui.videos;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class VideosViewModel extends ViewModel {

    private MutableLiveData<String> mText;

    public VideosViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("قسمت ویدیوها");
    }

    public LiveData<String> getText() {
        return mText;
    }
}