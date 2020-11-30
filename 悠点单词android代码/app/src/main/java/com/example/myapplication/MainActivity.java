package com.example.myapplication;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.MediaRouteButton;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.Toast;

import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;


public class MainActivity extends Activity {
    private Button btn1;
    private Button btn2;
    private Button btn3;
    private EditText editUser;
    private EditText editPass;
    private ProgressBar mBar;
    //
    public String txt;
    public String isOK;
    // 声明Sharedpreferenced对象
    private SharedPreferences sp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        btn1 = (Button)findViewById(R.id.button1);
        btn2 = (Button)findViewById(R.id.button2);
        btn3 = (Button)findViewById(R.id.button3);
        editUser = (EditText)findViewById(R.id.user);
        editPass = (EditText)findViewById(R.id.password);

        mBar = (ProgressBar) findViewById(R.id.mBar);
        mBar.setVisibility(View.INVISIBLE);

        btn1.setOnClickListener(new btn1_clock());
        btn2.setOnClickListener(new btn2_clock());
        btn3.setOnClickListener(new btn3_clock());
    }

    class btn1_clock implements View.OnClickListener
    {
        AlertDialog.Builder dialog=new AlertDialog.Builder(MainActivity.this);
        @Override
        public void onClick(View v)
        {
            //用户未输入
            if((editUser.getText().toString().equals(""))||(editPass.getText().toString().equals("")))
            {
                Toast.makeText(MainActivity.this,"账号和密码不能为空",Toast.LENGTH_SHORT).show();

            }else{
                mBar.setVisibility(View.VISIBLE);
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        RegisterActivity.User user = new RegisterActivity.User();
                        user.setPhone(editUser.getText().toString());
                        user.setPassword(editPass.getText().toString());
                        //okHttp 客户端
                        OkHttpClient client = new OkHttpClient();
                        //请求体---添加需要上传的字段
                        RequestBody requestBody = new FormBody.Builder()
                                .add("phone", user.phone)
                                .add("password", user.password)
                                .build();
                        //构建请求 添加本地ip地址 请求方式与后端相同
                        Request request = new Request.Builder()
                                .url("http://192.168.43.94:8000/youdian/lg/login/")//暂时
                                .post(requestBody)
                                .build();
                        try {
                            Response response = client.newCall(request).execute();
                                //请求处理,获取json字符串
                                String jsStr = response.body().string();
                                //解析json字符串
                                JSONObject object = new JSONObject(jsStr);
                                txt=object.getString("tx");
                                isOK = object.getString("isOK");
                                if(isOK.equals("OK"))
                                {
                                    Gson gson=new Gson();
                                    RegisterActivity.User user1;
                                    user1=gson.fromJson(jsStr, RegisterActivity.User.class);
                                    //把phone传给选择词库的页面，以便其请求服务器,下面那是文件名
                                    sp = getSharedPreferences("youDian", Context.MODE_PRIVATE);
                                    //获取到edit对象
                                    SharedPreferences.Editor edit = sp.edit();
                                    //通过editor对象写入数据
                                    edit.putString("phone",user1.phone.trim());
                                    System.out.println(user1.phone+user1.username+user1.email);
                                    edit.putString("username",user1.username.trim());
                                    edit.putString("email",user1.email.trim());
                                    //提交数据存入到xml文件中
                                    edit.commit();
                                    runOnUiThread(new Runnable() {
                                        @Override
                                        public void run() {
                                            mBar.setVisibility(View.INVISIBLE);
                                            Toast.makeText(MainActivity.this,"登录成功",Toast.LENGTH_SHORT).show();
                                            //跳转主页面
                                            Intent intent1=new Intent();
                                            intent1.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK|Intent.FLAG_ACTIVITY_NEW_TASK);
                                            intent1.setClass(MainActivity.this,MainActivity2.class);
                                            startActivity(intent1);
                                        }
                                    });
                                }
                                if(isOK.equals("NO"))
                                {
                                    runOnUiThread(new Runnable() {
                                        @Override
                                        public void run() {
                                            mBar.setVisibility(View.INVISIBLE);
                                            //设置对话框的标题
                                            dialog.setTitle("提示");
                                            //设置对话框显示的内容
                                            dialog.setMessage("登录失败，密码错误，或未注册");
                                            //设置对话框的“确定”按钮
                                            dialog.setPositiveButton("确定", new okClick());
                                            //创建对象框
                                            dialog.create();
                                            //显示对象框
                                            dialog.show();
                                        }
                                    });
                                }
                        }catch (IOException | JSONException e) {
                            e.printStackTrace();
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    mBar.setVisibility(View.INVISIBLE);
                                    //设置对话框的标题
                                    dialog.setTitle("提示");
                                    //设置对话框显示的内容
                                    dialog.setMessage("连接服务器失败，请稍后再试");
                                    //设置对话框的“确定”按钮
                                    dialog.setPositiveButton("确定", new okClick());
                                    //创建对象框
                                    dialog.create();
                                    //显示对象框
                                    dialog.show();
                                }
                            });
                        }
                    }
                }).start();
            }
        }
    }
    /*  普通对话框的“确定”按钮事件 */
    class okClick implements DialogInterface.OnClickListener
    {
        @Override
        public void onClick(DialogInterface dialog, int which)
        {
            dialog.cancel();
        }
    }
    class btn2_clock implements View.OnClickListener
    {
        @Override
        public void onClick(View v)
        {
            Intent intent=new Intent();
            intent.setClass(MainActivity.this,RegisterActivity.class);
            startActivity(intent);
        }
    }
    class btn3_clock implements View.OnClickListener
    {
        @Override
        public void onClick(View v)
        {
            Toast.makeText(MainActivity.this,"该功能暂不支持哦~",Toast.LENGTH_SHORT).show();
        }
    }
}