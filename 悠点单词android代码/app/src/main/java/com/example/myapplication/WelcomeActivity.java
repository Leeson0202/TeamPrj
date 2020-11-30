package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.WindowManager;

import java.util.Timer;
import java.util.TimerTask;

public class WelcomeActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);  //去掉状态栏，实现全屏
        setContentView(R.layout.activity_welcome);
        Timer timer=new Timer();
        TimerTask timerTask=new TimerTask() {
            @Override
            public void run() {
                Intent intent1=new Intent(WelcomeActivity.this, MainActivity.class);
                startActivity(intent1);
                WelcomeActivity.this.finish();
            }
        };
        timer.schedule(timerTask,1000*2);

    }
}