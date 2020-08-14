package com.example.myapplication;

import java.io.File;

public class Video {

    private String videoLink;
    private String videoName;

    public Video(String videoLink, String videoName) {
        this.videoLink = videoLink;
        this.videoName = videoName;
    }

    public String getVideoLink() { return videoLink; }

    public void setVideoLink(String videoLink) { this.videoLink = videoLink; }

    public String getVideoName() { return videoName; }

    public void setVideoName(String videoName) { this.videoName = videoName; }


}
