# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shel', '0011_auto_20160521_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(blank='True', null=True, upload_to='shelegram/media'),
        ),
    ]
