# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-26 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signupapplication', '0003_notification_seen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='seen',
            new_name='seenby',
        ),
        migrations.AddField(
            model_name='notification',
            name='seens',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
