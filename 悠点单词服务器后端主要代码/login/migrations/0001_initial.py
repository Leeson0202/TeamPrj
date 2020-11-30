# Generated by Django 3.1.2 on 2020-11-20 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('info', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='昵称')),
                ('password', models.CharField(max_length=256, verbose_name='用户密码')),
                ('email', models.EmailField(max_length=32, null=True, unique=True, verbose_name='用户邮箱')),
                ('phone', models.CharField(max_length=16, unique=True, verbose_name='用户手机号')),
                ('word_num', models.IntegerField(default=0, verbose_name='用户词汇量')),
                ('false_word', models.TextField(null=True, verbose_name='易错单词')),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('user_info', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to='info.info', verbose_name='签名')),
            ],
            options={
                'db_table': 'user',
                'ordering': ['c_time'],
            },
        ),
    ]
