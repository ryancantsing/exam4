# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-05 22:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20180104_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='added_by', to='exam.Users'),
        ),
        migrations.AlterField(
            model_name='items',
            name='wished_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wished_for', to='exam.Users'),
        ),
    ]
