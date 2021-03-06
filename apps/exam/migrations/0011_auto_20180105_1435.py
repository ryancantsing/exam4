# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-05 22:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0010_auto_20180105_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='items',
            name='wished_for',
        ),
        migrations.AddField(
            model_name='users',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='added_by', to='exam.Items'),
        ),
        migrations.AddField(
            model_name='users',
            name='wished_for',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wished_for', to='exam.Items'),
        ),
    ]
