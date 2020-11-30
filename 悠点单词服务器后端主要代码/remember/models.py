from django.db import models


# Create your models here.


class word(models.Model):
    spell = models.CharField(max_length=256, verbose_name='拼写')
    tag = models.CharField(max_length=128, verbose_name='标签')
    clearfix = models.TextField(verbose_name='词性与翻译')
    sentence = models.TextField(verbose_name='列句')

    class Meta:
        db_table = 'word'
