# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-19 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shel', '0002_auto_20160518_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
    ]