# Generated by Django 3.1.2 on 2020-11-20 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spell', models.CharField(max_length=256, verbose_name='拼写')),
                ('tag', models.CharField(max_length=128, verbose_name='标签')),
                ('clearfix', models.TextField(verbose_name='词性与翻译')),
                ('sentence', models.TextField(verbose_name='列句')),
            ],
            options={
                'db_table': 'word',
            },
        ),
    ]
