# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-10 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20170710_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseresource',
            name='name',
            field=models.CharField(max_length=50, verbose_name='资源名称'),
        ),
    ]
