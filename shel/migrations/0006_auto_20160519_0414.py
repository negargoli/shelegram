# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shel', '0005_auto_20160519_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(blank='True', null=True, upload_to='media/'),
        ),
    ]
