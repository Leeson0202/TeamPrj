package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.PendingIntent;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;

import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;

import org.jetbrains.annotations.NotNull;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.List;

import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class ChooseDicActivity extends Activity {
    private Button btn;
    private RadioButton gk,c4,c6;
    private TextView now_dic;
    private ProgressBar mBar1;
    private static String tag;//记录用户选择的词库
//    boolean isFirstIn = true;
//    private SharedPreferences.Editor edit;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choose_dic);
        btn = (Button)findViewById(R.id.chooseDic_btn);
        gk = (RadioButton)findViewById(R.id.gaokao_rb);
        c4 = (RadioButton)findViewById(R.id.siji_rb);
        c6 = (RadioButton)findViewById(R.id.liuji_rb);
        now_dic=(TextView)findViewById(R.id.now_dic);
        mBar1=(ProgressBar)findViewById(R.id.mBar1);
        mBar1.setVisibility(View.INVISIBLE);
        SharedPreferences sp1 ;
        sp1 = getSharedPreferences("youDian", Context.MODE_PRIVATE);
        now_dic.setText("当前词库："+sp1.getString("Tag","待选"));
        btn.setOnClickListener(new btn_clock());
    }
    class btn_clock implements View.OnClickListener
    {
        @Override
        public void onClick(View v)
        {
            switch (CASE()){
                case 0://没有选择
                    Toast.makeText(ChooseDicActivity.this, "请选择词库", Toast.LENGTH_SHORT).show();
                    break;
                default://选择了就导入
                    mBar1.setVisibility(View.VISIBLE);
                    imp(tag);
                    //并把tag保存在sharedpreferenced，以便mainActivity2读取相应的词库
                    SharedPreferences sp ;
                    sp = getSharedPreferences("youDian", Context.MODE_PRIVATE);
                    //获取到edit对象
                    SharedPreferences.Editor edit = sp.edit();
                    //通过editor对象写入数据
                    edit.putString("Tag",tag.trim());
                    //提交数据存入到xml文件中
                    edit.commit();
                    break;
            }
            }

    }
    //if改switch的目的 来选择radiobutton
    public int CASE(){
        int a=0;
        if(gk.isChecked())
        {
            a=1;
            tag="高中";
        }
        if(c4.isChecked())
        {
            a=2;
            tag="CET4";
        }
        if(c6.isChecked())
        {
            a=3;
            tag="CET6";
        }
        return a;
    }
    //导入词库并保存在本地的方法
    public void imp(final String tag){
        //先抛一个网络请求的线程
        new Thread(new Runnable() {
            @Override
            public void run() {
                OkHttpClient client = new OkHttpClient();
                //上传当前登录者的手机账号和选择的tag即词库
                //先得到当前登陆者的手机账号，由登录页面传来
                SharedPreferences sp = getSharedPreferences("youDian",Context.MODE_PRIVATE);
                String userPhone=sp.getString("phone",null);
                if(userPhone==null){
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(ChooseDicActivity.this,"获取账户失败;bundle:null", Toast.LENGTH_SHORT).show();
                        }
                    });
                }
                else{
                    //继续网络请求
                RequestBody requestBody = new FormBody.Builder()
                        .add("phone",userPhone)
                        .add("tag",tag)
                        .build();
                //构建请求
                Request request = new Request.Builder()
                        .url("http://192.168.43.94:8000/youdian/word/select/")//暂时
                        .post(requestBody)
                        .build();
                try{
                    Response response = client.newCall(request).execute();
                    String jsonString=response.body().string();
                    //处理请求结果
                    //通过isOK定制不同的json2user对象
                    String isOK;
                    JSONObject obj=new JSONObject(jsonString);
                    isOK=obj.getString("isOK");
                    if(isOK.equals("NO")){
                        //服务器发生错误
                        //ui做出反应
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(ChooseDicActivity.this,"服务器发生错误", Toast.LENGTH_SHORT).show();
                            }
                        });
                    }
                    else{
                        //请求正常，那就先把jsonString保存在本地,主页背词时直接读取本地文件
                        saveFile(tag,jsonString);
                    }
                }catch (IOException | JSONException e){
                    e.printStackTrace();
                    Toast.makeText(ChooseDicActivity.this, "连接服务器失败，请稍后重试", Toast.LENGTH_SHORT).show();
                }
                }
            }
        }).start();
    }
    public void saveFile(String tag, @NotNull String jsonString){
        String fileName=tag+".txt";
        FileOutputStream f_out;
        try{
            f_out=openFileOutput(fileName,Context.MODE_PRIVATE);
            f_out.write(jsonString.getBytes());
            //提示保存成功
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mBar1.setVisibility(View.INVISIBLE);
                    AlertDialog.Builder dialog=new AlertDialog.Builder(ChooseDicActivity.this);
                    //设置对话框的标题
                    dialog.setTitle("提示");
                    //设置对话框显示的内容
                    dialog.setMessage("导入成功");
                    //设置对话框的“确定”按钮
                    dialog.setPositiveButton("返回主页", new okClick());
                    //创建对象框
                    dialog.create();
                    //显示对象框
                    dialog.show();
                }
            });
        }catch (FileNotFoundException e){
            e.printStackTrace();
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mBar1.setVisibility(View.INVISIBLE);
                    Toast.makeText(ChooseDicActivity.this,"导入失败：FileNotFoundException", Toast.LENGTH_SHORT).show();
                }
            });
        }
         catch (IOException e){
            e.printStackTrace();
             runOnUiThread(new Runnable() {
                 @Override
                 public void run() {
                     mBar1.setVisibility(View.INVISIBLE);
                     Toast.makeText(ChooseDicActivity.this,"导入失败：IOException", Toast.LENGTH_SHORT).show();
                 }
             });
        }
    }
    class okClick implements DialogInterface.OnClickListener
    {
        @Override
        public void onClick(DialogInterface dialog, int which)
        {
            Intent intent=new Intent();
            intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK|Intent.FLAG_ACTIVITY_NEW_TASK);
            intent.setClass(ChooseDicActivity.this,MainActivity2.class);
            startActivity(intent);
        }
    }
}