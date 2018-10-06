# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-10-06 05:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+8888888888'.Min. 8 digits.Max. 15 digits.", regex='^\\+\\d{8,15}$')]),
        ),
    ]
