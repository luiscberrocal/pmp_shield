# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-21 23:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_load_offices'),
        ('projects', '0002_auto_20160821_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='employees.OrganizationUnit', verbose_name='office in charge'),
        ),
    ]
