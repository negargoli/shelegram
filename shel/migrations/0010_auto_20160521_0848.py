# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-21 15:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shel', '0009_remove_membership_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupadmin', to='shel.Person'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupid', to='shel.Group'),
        ),
    ]
