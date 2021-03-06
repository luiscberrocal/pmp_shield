# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-01 22:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0002_load_offices'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('grade_type', models.CharField(max_length=2, verbose_name='grade type')),
                ('level', models.IntegerField(verbose_name='level')),
            ],
            options={
                'ordering': ('grade_type', 'level'),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.CharField(max_length=6, unique=True, verbose_name='position number')),
                ('tenure', models.CharField(choices=[('P', 'Permanent'), ('T', 'Temporary')], default='T', max_length=1, verbose_name='tenure')),
                ('current_office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='employees.OrganizationUnit', verbose_name='current office')),
                ('current_owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permanent_position', to='employees.Employee', verbose_name='current owner')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='positions.GradeLevel', verbose_name='grade')),
            ],
            options={
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='PositionDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=120)),
                ('short_name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PositionEmployeeAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('planned_start_date', models.DateField()),
                ('planned_end_date', models.DateField()),
                ('actual_start_date', models.DateField(blank=True, null=True)),
                ('actual_end_date', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_assignments', to='employees.Employee')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_assignments', to='positions.Position')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='position',
            name='position_description',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='positions.PositionDescription', verbose_name='position description'),
        ),
        migrations.AlterUniqueTogether(
            name='gradelevel',
            unique_together=set([('grade_type', 'level')]),
        ),
    ]
