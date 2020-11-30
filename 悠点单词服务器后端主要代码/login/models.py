from django.db import models
from info.models import Info


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='昵称')
    password = models.CharField(max_length=256, verbose_name='用户密码')
    email = models.EmailField(max_length=32, unique=True, verbose_name='用户邮箱', null=True)
    phone = models.CharField(max_length=16, unique=True, verbose_name='用户手机号')

    word_num = models.IntegerField(verbose_name='用户词汇量', default=0)
    false_word = models.TextField(null=True, verbose_name='易错单词')

    user_info = models.OneToOneField(to=Info, null=True, related_name='user_info', verbose_name='签名',
                                     on_delete=models.CASCADE)

    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'
        ordering = ['c_time']
