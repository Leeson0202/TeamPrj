package com.example.myapplication.ui.notifications;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.Toolbar;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.example.myapplication.MainActivity2;
import com.example.myapplication.R;
import com.example.myapplication.ui.home.HomeFragment;
import com.example.myapplication.ui.home.HomeViewModel;

public class NotificationsFragment extends Fragment {

    private NotificationsViewModel notificationsViewModel;
    public TextView v6;
    public TextView v7;
    public TextView v8;
    public static View root=null;//要是静态变量
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        if (null != root) {
            ViewGroup parent = (ViewGroup) root.getParent();
            if (null != parent) {
                parent.removeView(root);
            }
        } else {
            root = inflater.inflate(R.layout.fragment_notifications, container, false);
            initView(root);// 控件初始化
        }
        return root;
    }

    public void initView(View root){
        notificationsViewModel = new ViewModelProvider(this).get(NotificationsViewModel.class);
        v6=(TextView)root.findViewById(R.id.textView6);
        v7=(TextView)root.findViewById(R.id.textView7);
        v8=(TextView)root.findViewById(R.id.textView8);
        SharedPreferences sp;
        sp = activity.getSharedPreferences("youDian", Context.MODE_PRIVATE);
        v6.setText("昵称："+sp.getString("username",null));
        v7.setText("账号："+sp.getString("phone",null));
        v8.setText("email："+sp.getString("email",null));
    }

    //防止fragment的getActivity（）为空，用下面的activity代替getActivity();
    public Activity activity;
    @Override
    public void onAttach(Context context){
        super.onAttach(context);
        activity=(Activity)context;
    }
}