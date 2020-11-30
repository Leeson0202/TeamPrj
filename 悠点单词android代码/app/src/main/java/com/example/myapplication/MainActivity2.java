package com.example.myapplication;

import android.app.Activity;
import android.app.ActivityManager;
import android.app.AlertDialog;
import android.content.ClipData;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.view.animation.Animation;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.myapplication.ui.dashboard.DashboardFragment;
import com.example.myapplication.ui.home.HomeFragment;
import com.example.myapplication.ui.notifications.NotificationsFragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.gson.Gson;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.fragment.NavHostFragment;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import org.jetbrains.annotations.NotNull;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.util.List;

public class MainActivity2 extends AppCompatActivity {
//
//    private BottomNavigationView bottomNavigationView;
//    private Fragment fragment1;
//    private Fragment fragment2;
//    private Fragment fragment3;
//    private Fragment[] fragments;
//    private int lastfragment;//用于记录上个选择的Fragment

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        BottomNavigationView navView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        AppBarConfiguration appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_reciteWord, R.id.navigation_community, R.id.navigation_myInfo)
                .build();

        navView.setOnNavigationItemSelectedListener( mOnNavigationItemSelectedListener );
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment);
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);



    }
    //实现点击两次退出app
    private static final int TIME_EXIT=2000;
    private long mBackPressed;
    @Override
    public void onBackPressed(){
        if(mBackPressed+TIME_EXIT>System.currentTimeMillis()){
            super.onBackPressed();
            return;
        }else{
            Toast.makeText(this,"再点一次返回键退出",Toast.LENGTH_SHORT).show();
            mBackPressed=System.currentTimeMillis();
        }
    }


    private FragmentTransaction transaction;
    private FragmentManager fragmentManager;
    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {
        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            fragmentManager = getSupportFragmentManager();  //使用fragmentManager和transaction来实现切换效果
            transaction = fragmentManager.beginTransaction();
            switch (item.getItemId()) {
                case R.id.navigation_reciteWord:
                    transaction.replace(R.id.content,new HomeFragment());  //对应的java class
                    transaction.commit();  //一定不要忘记commit，否则不会显示
                    return true;
                case R.id.navigation_community:

                    return true;
                case R.id.navigation_myInfo:

                    return true;
            }
            return false;
        }
    };
    // 设置默认进来是tab 显示的页面
    private void setDefaultFragment(){
        fragmentManager = getSupportFragmentManager();
        transaction = fragmentManager.beginTransaction();
        transaction.replace(R.id.content,new HomeFragment());
        transaction.commit();
    }

}
