from django.db import models


# Create your models here.


class Info(models.Model):
    scripts = models.TextField(verbose_name='个性签名')

    class Meta:
        db_table = 'Info'