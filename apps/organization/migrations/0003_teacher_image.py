# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-07 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_courseorg_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='teacher/%Y/%m', verbose_name='教师头像'),
        ),
    ]