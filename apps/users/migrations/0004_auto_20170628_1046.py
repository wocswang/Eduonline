# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-28 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170626_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailvertifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('update_mail', '修改邮箱')], default='register', max_length=30, verbose_name='类型'),
        ),
    ]
