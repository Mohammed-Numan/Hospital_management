# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0009_remove_appointment_lastvisited'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='Email',
            field=models.CharField(default='hello@gmail.com', max_length=30),
            preserve_default=False,
        ),
    ]
