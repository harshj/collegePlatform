# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-24 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signupapplication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='rank',
            field=models.IntegerField(),
        ),
    ]
