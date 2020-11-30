import storage from '@system.storage';
import router from '@system.router';
import file from '@system.file';
import request from '@system.request';
import fetch from '@system.fetch';
import app from '@system.app';
import network from '@system.network';
import sensor from '@system.sensor';
import prompt from '@system.prompt';
export default{
    data:{
        tittle : 0,
        log: '欢迎来到悠点单词！',
    },
    link(){
        let me =this;
        fetch.fetch({
            url: 'http://192.168.43.251:8000/youdian/lg/register/',
            method:'POST',
            header:{
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data:{
                username: 'abc',
                password: '123456',
                email:'1111111111@qq.com',
                phone:'11111111111'
            },
            success: function(response) {
                console.log('response code:' + response.code);
                console.log('response data:' + response.data);
            },
            fail: function(data, code) {
                console.log('fail callback');
            },
        });
    },
    myon(){
        prompt.showToast({
            message: '登录成功！',
        });
        var timeoutID = setTimeout(function() {
            router.replace({
                uri:'pages/tip/tip'
            });
        }, 2000);
    },

}

