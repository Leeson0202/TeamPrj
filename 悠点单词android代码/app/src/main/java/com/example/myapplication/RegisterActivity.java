package com.example.myapplication;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
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

public class RegisterActivity extends Activity {

    private Button r_btn;
    private EditText r_id;
    private EditText r_pass;
    private EditText r_name;
    private EditText r_email;
    private ProgressBar mBar2;
    //定义一个用户类
    public static class User implements java.io.Serializable {
        public String phone;//id是手机号
        public String password;//密码
        public String email;//邮箱
        public String username;//昵称
        public String tag;//词库标签
        public String false_word;//易错单词
        public String info;//个性签名


        public User() {
            this.phone = phone;//phone
            this.password = password;//password
            this.email = email;//email
            this.username = username;//username
            this.tag = tag;
            this.false_word = false_word;
            this.info = info;
        }

        public String getPhone() {
            return phone;
        }
        public void setPhone(String phone) {
            this.phone = phone;
        }

        public String getPassword() {
            return password;
        }
        public void setPassword(String password) {
            this.password = password;
        }

        public String getEmail() {
            return email;
        }
        public void setEmail(String email) {
            this.email = email;
        }

        public String getName() {
            return username;
        }
        public void setName(String username) {
            this.username = username;
        }

        public String getTag() {
            return tag;
        }
        public void setTag(String tag) {
            this.tag = tag;
        }

        public String getFalse_word() {
            return false_word;
        }
        public void setFalse_word(String false_word) {
            this.false_word = false_word;
        }

        public String getInfo() {
            return info;
        }
        public void setInfo(String info) {
            this.info = info;
        }
    }

    //接受由json转过来的数据
    public String txt="";
    public String isOK="";

        @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        r_btn = (Button) findViewById(R.id.register_button);
        r_id = (EditText) findViewById(R.id.register_id);
        r_pass = (EditText) findViewById(R.id.register_Password);
        r_name = (EditText) findViewById(R.id.register_name);
        r_email = (EditText) findViewById(R.id.register_email);
        mBar2=(ProgressBar)findViewById(R.id.mBar2);
        mBar2.setVisibility(View.INVISIBLE);
        r_btn.setOnClickListener(new r_btn_clock());
    }

    public class r_btn_clock implements View.OnClickListener {
        AlertDialog.Builder dialog = new AlertDialog.Builder(RegisterActivity.this);
        @Override
        public void onClick(View v) {
            //用户点击按钮，判断从EditText传来的数据
            //数据为空，说明用户未输入
            if (r_id.getText().toString().equals("") || r_pass.getText().toString().equals("") || r_name.getText().toString().equals("")||r_email.getText().toString().equals("")) {
                Toast.makeText(RegisterActivity.this,"输入内容不能为空",Toast.LENGTH_SHORT).show();
            } else//不为空，用户已经输入数据，就把数据在子线程传给新建user并传给user后上传user到服务器
            {
                mBar2.setVisibility(View.VISIBLE);
                //新建子线程
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        User user = new User();
                        user.setPhone(r_id.getText().toString());
                        user.setPassword(r_pass.getText().toString());
                        user.setName(r_name.getText().toString());
                        user.setEmail(r_email.getText().toString());//非必填项
                        //okHttp 客户端
                        OkHttpClient client = new OkHttpClient();
                        //请求体---添加需要上传的字段
                        RequestBody requestBody = new FormBody.Builder()
                                .add("username", user.username)
                                .add("password", user.password)
                                .add("email", user.email)
                                .add("phone", user.phone)
                                .build();
                        //构建请求 添加本地ip地址 请求方式与后端相同
                        Request request = new Request.Builder()
                                .url("http://192.168.43.94:8000/youdian/lg/register/")//暂时
                                .post(requestBody)
                                .build();
                        try {
                            Response response = client.newCall(request).execute();
                            //请求处理,获取json字符串
                            String jsonString = response.body().string();
                            //解析json字符串
                            JSONObject object = new JSONObject(jsonString);
                            txt = object.getString("tx");
                            isOK = object.getString("isOK");
                        } catch (IOException | JSONException e) {
                            e.printStackTrace();
                        }
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                if(isOK.equals("OK")) {
                                    mBar2.setVisibility(View.INVISIBLE);
                                    //设置对话框的标题
                                    dialog.setTitle("提示");
                                    //设置对话框显示的内容
                                    dialog.setMessage(txt);
                                    //设置对话框的“确定”按钮
                                    dialog.setPositiveButton("立即登录", new okClick());
                                    //创建对象框
                                    dialog.create();
                                    //显示对象框
                                    dialog.show();
                                }
                                if(isOK.equals("NO"))
                                {
                                    mBar2.setVisibility(View.INVISIBLE);
                                    //设置对话框的标题
                                    dialog.setTitle("提示");
                                    //设置对话框显示的内容
                                    dialog.setMessage(txt);
                                    //设置对话框的“确定”按钮
                                    dialog.setPositiveButton("稍后再试", new Not_okClick());
                                    //创建对象框
                                    dialog.create();
                                    //显示对象框
                                    dialog.show();
                                }
                                if(isOK.equals("")){
                                    mBar2.setVisibility(View.INVISIBLE);
                                    //设置对话框的标题
                                    dialog.setTitle("提示");
                                    //设置对话框显示的内容
                                    dialog.setMessage("连接服务器失败，请稍后再试");
                                    //设置对话框的“确定”按钮
                                    dialog.setPositiveButton("确定", new Not_okClick());
                                    //创建对象框
                                    dialog.create();
                                    //显示对象框
                                    dialog.show();
                                }
                            }
                        });
                    }
                }).start();

                }
            }
        }

    static class Not_okClick implements DialogInterface.OnClickListener {

        @Override
        public void onClick(DialogInterface dialog, int which) {
            dialog.cancel();
        }
    }

    class okClick implements DialogInterface.OnClickListener {

        @Override
        public void onClick(DialogInterface dialog, int which) {
            Intent intent = new Intent();
            intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_NEW_TASK);
            intent.setClass(RegisterActivity.this, MainActivity.class);
            startActivity(intent);
        }
    }

}