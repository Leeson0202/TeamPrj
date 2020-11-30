import storage from '@system.storage';
import router from '@system.router';
import file from '@system.file';
import request from '@system.request';
import fetch from '@system.fetch';
import network from '@system.network';
import prompt from '@system.prompt';
export default{
    data:{
        tittle : 0,
        spell: 'apple',
        abc: '苹果',
        a:0,
    },
    run(){
        var a=0;
        a++;
        this.tittle=this.tittle+5/600;
        if (this.tittle>=100) {
            clearInterval(this.timer);
            this.tittle=0;
        }
    },
    myon(){
        var timer=setInterval(this.run,5);
    },
    next(){
        var my=[];
        var b=this.a;
        my=this.$t('strings.mywords');
        this.spell=my[b].spell;
        this.abc=my[b].clearfix;
        this.a++
    },
    stop(){
        var c=this.a+1;
        var b=c.toString();
        prompt.showToast({
            message: '本次一共背了'+b+'个单词！',
        });
        var timeoutID = setTimeout(function() {
            router.replace({
                uri:'pages/tip/tip'
            })
        }, 2000);
    },
}
