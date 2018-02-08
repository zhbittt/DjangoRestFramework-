# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-07 10:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=64)),
                ('token', models.CharField(blank=True, max_length=64, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_serializers.Group')),
                ('roles', models.ManyToManyField(to='app_serializers.Roles')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_serializers.Menu'),
        ),
    ]