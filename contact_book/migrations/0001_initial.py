# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-10-06 05:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date joined ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('soft_delete', models.BooleanField(default=False, verbose_name='soft delete')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+8888888888'. Max. 15 digits.", regex='^\\+\\d{8,15}$')])),
            ],
            options={
                'db_table': 'contacts',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TokenValidation',
            fields=[
                ('token_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date joined ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('soft_delete', models.BooleanField(default=False, verbose_name='soft delete')),
                ('email', models.EmailField(max_length=254)),
                ('token_md5', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'token_validation',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date joined ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('soft_delete', models.BooleanField(default=False, verbose_name='soft delete')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('name', 'email')]),
        ),
    ]
