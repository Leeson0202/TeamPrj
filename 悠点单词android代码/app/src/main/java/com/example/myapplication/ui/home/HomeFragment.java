package com.example.myapplication.ui.home;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.AssetManager;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.provider.SyncStateContract;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.Animation;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.widget.Toolbar;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentContainerView;
import androidx.fragment.app.FragmentManager;
import androidx.lifecycle.ViewModelProvider;
import com.example.myapplication.ChooseDicActivity;
import com.example.myapplication.MainActivity2;
import com.example.myapplication.R;
import com.google.gson.Gson;

import org.jetbrains.annotations.NotNull;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.reflect.Field;
import java.util.List;

public class HomeFragment extends Fragment {
    private HomeViewModel homeViewModel;
    private Toolbar mToolbar;
    public ImageButton btn;
    public ImageView clock;//倒计时图片
    public TextView num;//倒计时
    public TextView spell;
    public TextView tag;
    public TextView clearFix;
    public TextView sentence;
    public ImageButton get;
    public ImageButton pass;
    public TextView getNum;
    public TextView passNum;
    public TextView tip;
    public TextView tip2;
    public class Rec implements java.io.Serializable{
        String isOK;//无用
        String tx;//无用
        List<Word> word;
        public Rec(){
            this.isOK=getIsOK();
            this.tx=getTx();
            this.word=getWord();
        }
        public String getIsOK(){
            return isOK;
        }
        public void setIsOK(String isOK){
            this.isOK=isOK;
        }
        public String getTx(){
            return tx;
        }
        public void setTx(String tx){
            this.tx=tx;
        }
        public List<Word> getWord(){
            return word;
        }
        public void setWordList(List<Word> word){
            this.word=word;
        }
    }
    public class Word implements java.io.Serializable{
        int id;
        String spell;//单词拼写
        String tag;//单词词库标签
        String clearfix;//词性与意思
        String sentence;//例句
        public Word(){
            this.id=getId();
            this.spell=getSpell();
            this.tag=getTag();
            this.clearfix=getClearfix();
            this.sentence=getSentence();
        }
        public int getId(){
            return id;
        }
        public void setId(int id){
            this.id=id;
        }
        public String getSpell(){
            return spell;
        }
        public void setSpell(String spell){
            this.spell=spell;
        }
        public String getTag(){
            return tag;
        }
        public void setTag(String tag){
            this.tag=tag;
        }
        public String getClearfix(){
            return clearfix;
        }
        public void setClearfix(String clearfix){
            this.clearfix=clearfix;
        }
        public String getSentence(){
            return sentence;
        }
        public void setSentence(String sentence){
            this.sentence=sentence;
        }
    }
    int order=0;//单词位置，可从登录的用户数据里获得
    static int g=0,p=0;

    //防止页面切换后fragment重复刷新,需要是static
    public static View view=null;
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        //始终显示右上角菜单
        setHasOptionsMenu(true);
        if (null != view) {
            ViewGroup parent = (ViewGroup) view.getParent();
            if (null != parent) {
                parent.removeView(view);
            }
        } else {
            view = inflater.inflate(R.layout.fragment_home, container, false);
            initView(view);// 控件初始化
        }
        return view;
    }

    //防止fragment的getActivity（）为空，用下面的activity代替getActivity();
    //防止快速切换fragment时程序闪退，但是好像并没有什么卵用，以后还得改
    public Activity activity;
    @Override
    public void onAttach(Context context){
        super.onAttach(context);
        activity=(Activity)context;
    }

    public void initView(View root){
        //initial
        homeViewModel = new ViewModelProvider(this).get(HomeViewModel.class);
        mToolbar = root.findViewById(R.id.mToolbar);
        clock=(ImageView)root.findViewById(R.id.clock);
        btn = (ImageButton)root.findViewById(R.id.btn);
        num = (TextView)root.findViewById(R.id.num);
        spell=(TextView)root.findViewById(R.id.spell);
        tag=(TextView)root.findViewById(R.id.Tag);
        clearFix=(TextView)root.findViewById(R.id.clearFix);
        sentence=(TextView)root.findViewById(R.id.sentence);
        get=(ImageButton)root.findViewById(R.id.get);
        pass=(ImageButton)root.findViewById(R.id.pass);
        getNum=(TextView)root.findViewById(R.id.getNum);
        passNum=(TextView)root.findViewById(R.id.passNum);
        tip=(TextView)root.findViewById(R.id.tip);
        tip2=(TextView)root.findViewById(R.id.tip2);
        btn.setOnClickListener(new okClick());
        get.setOnClickListener(new okClick1());
        pass.setOnClickListener(new okClick2());
        //先设置隐藏
        tip2.setVisibility(View.INVISIBLE);
        clock.setVisibility(View.INVISIBLE);
        num.setVisibility(View.INVISIBLE);
        tag.setVisibility(View.INVISIBLE);
        spell.setVisibility(View.INVISIBLE);
        clearFix.setVisibility(View.INVISIBLE);
        sentence.setVisibility(View.INVISIBLE);
        passNum.setVisibility(View.INVISIBLE);
        getNum.setVisibility(View.INVISIBLE);
        pass.setVisibility(View.INVISIBLE);
        get.setVisibility(View.INVISIBLE);
    }
    Rec rec=new Rec();
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        inflater.inflate(R.menu.reciteword, menu);
        super.onCreateOptionsMenu(menu, inflater);
    }
    class okClick implements View.OnClickListener {

        @Override
        public void onClick(View v) {
            //先读取词库
            String jsonString = readFileData();
            //解析jsonString到对象Rec
            Gson gson = new Gson();
            rec = gson.fromJson(jsonString, Rec.class);
            if (rec == null) {
                Toast.makeText(activity, "请先选择单词库", Toast.LENGTH_SHORT).show();
            } else {
                tip.setVisibility(View.INVISIBLE);
                tip2.setVisibility(View.VISIBLE);
                clock.setVisibility(View.VISIBLE);
                num.setVisibility(View.VISIBLE);
                btn.setVisibility(View.INVISIBLE);
                //倒计时开始
                timer0.start();

            }
    }
    }

    class okClick1 implements View.OnClickListener {
        @Override
        public void onClick(View v) {
            order++;g++;
            spell.setText(rec.word.get(order).spell);
            tag.setText("等级：\n"+rec.word.get(order).tag);
            clearFix.setText("释义：\n"+rec.word.get(order).clearfix);
            sentence.setText("例句：\n"+rec.word.get(order).sentence);
            //设置sentence可滑动
            sentence.setMovementMethod(ScrollingMovementMethod.getInstance());
            getNum.setText(String.valueOf(g));
        }
    }
    class okClick2 implements View.OnClickListener {
        @Override
        public void onClick(View v) {
            order++;p++;
            spell.setText(rec.word.get(order).spell);
            tag.setText("等级：\n"+rec.word.get(order).tag);
            clearFix.setText("释义：\n"+rec.word.get(order).clearfix);
            sentence.setText("例句：\n"+rec.word.get(order).sentence);
            //设置sentence可滑动
            sentence.setMovementMethod(ScrollingMovementMethod.getInstance());
            passNum.setText(String.valueOf(p));
        }
    }
    public String readFileData(){
        String result=null;
        SharedPreferences sp = activity.getSharedPreferences("youDian",Context.MODE_PRIVATE);
        String tag=sp.getString("Tag",null);
            String fileName=tag+".txt";
            try{
                FileInputStream fis = activity.openFileInput(fileName);
                //获取文件长度
                int length = fis.available();
                byte[] buffer = new byte[length];
                fis.read(buffer);
                //将byte数组转换成指定格式的字符串
                result = new String(buffer, "UTF-8");
            } catch (Exception e) {
                e.printStackTrace();//此时返回result为null
                }
        return  result;
    }
    //计数器0
    public CountDownTimer timer0 = new CountDownTimer(6000, 1000) {
        @Override
        public void onTick(long millisUntilFinished) {
            num.setText(String.valueOf(millisUntilFinished/1000));
        }
        @Override
        public void onFinish() {
            tip2.setVisibility(View.INVISIBLE);
            tag.setVisibility(View.VISIBLE);
            spell.setVisibility(View.VISIBLE);
            clearFix.setVisibility(View.VISIBLE);
            sentence.setVisibility(View.VISIBLE);
            passNum.setVisibility(View.VISIBLE);
            getNum.setVisibility(View.VISIBLE);
            pass.setVisibility(View.VISIBLE);
            get.setVisibility(View.VISIBLE);
            //结束后再计时
            timer.start();
            //开始背词
            ReciteWord(rec, order);
        }
    };
    //计数器
    public CountDownTimer timer = new CountDownTimer(61000, 1000) {
        @Override
        public void onTick(long millisUntilFinished) {
            num.setText(String.valueOf(millisUntilFinished/1000));
        }
        @Override
        public void onFinish() {
            AlertDialog.Builder dialog = new AlertDialog.Builder(activity);
            //设置对话框的标题
            dialog.setTitle("挑战结束");
            //设置对话框显示的内容
            dialog.setMessage("本次记住"+g+"个单词，跳过"+p+"个单词，再接再厉！");
            //设置对话框的“确定”按钮
            dialog.setPositiveButton("确定", new DialogOkClick());
            //创建对象框
            dialog.create();
            //显示对象框
            dialog.show();
            clock.setVisibility(View.INVISIBLE);
            num.setVisibility(View.INVISIBLE);
            tag.setVisibility(View.INVISIBLE);
            spell.setVisibility(View.INVISIBLE);
            clearFix.setVisibility(View.INVISIBLE);
            sentence.setVisibility(View.INVISIBLE);
            passNum.setVisibility(View.INVISIBLE);
            getNum.setVisibility(View.INVISIBLE);
            pass.setVisibility(View.INVISIBLE);
            get.setVisibility(View.INVISIBLE);
            btn.setVisibility(View.VISIBLE);
            tip.setVisibility(View.VISIBLE);
        }
    };
    class DialogOkClick implements DialogInterface.OnClickListener {
        @Override
        public void onClick(DialogInterface dialog, int which) {
            dialog.cancel();
        }
    }
    public void ReciteWord(Rec rec,int i){
        //int i是开始背单词时的单词位置或顺序，即从第i个单词开始背起
            spell.setText(rec.word.get(i).spell);
            tag.setText("等级：\n"+rec.word.get(i).tag);
            clearFix.setText("释义：\n"+rec.word.get(i).clearfix);
            sentence.setText("例句：\n"+rec.word.get(i).sentence);
            //设置sentence可滑动
            sentence.setMovementMethod(ScrollingMovementMethod.getInstance());
    }
    public boolean onOptionsItemSelected(@NotNull MenuItem item) {
        Intent intent = new Intent();
        intent.setClass(activity, ChooseDicActivity.class);
        switch (item.getItemId()) {
            case R.id.c1:
                startActivity(intent);
                break;
            case R.id.c2:
                Toast.makeText(activity, "还没来得及开发嘤~", Toast.LENGTH_SHORT).show();
                break;
            case R.id.c3:
                Toast.makeText(activity, "为时60s，每记住一个单词请按“√”，跳过请按“×”。一经开始，恕不暂停(￣^￣)。", Toast.LENGTH_LONG).show();
                break;
            default:
                break;
        }
        return true;
    }
}