# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-22 03:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190322_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='title',
            field=models.CharField(max_length=10, null=True),
        ),
    ]