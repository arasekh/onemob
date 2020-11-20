package com.example.myapplication;

public class QuizResult {
    private String yourSelectedSwitch;
    private String trueSwitch;

    public QuizResult(String yourSelectedSwitch, String trueSwitch) {
        this.yourSelectedSwitch = yourSelectedSwitch;
        this.trueSwitch = trueSwitch;
    }

    public String getYourSelectedSwitch() { return yourSelectedSwitch; }

    public void setYourSelectedSwitch(String yourSelectedSwitch) { this.yourSelectedSwitch = yourSelectedSwitch; }

    public String getTrueSwitch() { return trueSwitch; }

    public void setTrueSwitch(String trueSwitch) { this.trueSwitch = trueSwitch; }
}
