# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 14:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0012_auto_20161013_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='title',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='image',
        ),
        migrations.AddField(
            model_name='images',
            name='ad',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ads.Ad'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]