# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 03:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encryptly_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
