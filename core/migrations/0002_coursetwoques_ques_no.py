# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetwoques',
            name='ques_no',
            field=models.IntegerField(default=0),
        ),
    ]
