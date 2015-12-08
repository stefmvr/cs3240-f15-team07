# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('owner', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('parent_folder', models.ForeignKey(null=True, blank=True, to='login.Folder')),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('group_name', models.CharField(max_length=100)),
                ('group_creator', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MessageDB',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('message_subject', models.CharField(max_length=100)),
                ('message_body', models.TextField(max_length=5000)),
                ('encrypted', models.BooleanField()),
                ('sym_password', models.BinaryField()),
                ('sent_date', models.DateTimeField()),
                ('unread', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('report_title', models.CharField(max_length=100)),
                ('report_body', models.TextField(max_length=5000)),
                ('report_private', models.BooleanField()),
                ('report_owner', models.CharField(default='', max_length=100)),
                ('report_timestamp', models.DateTimeField(auto_now_add=True)),
                ('parent_folder', models.ForeignKey(null=True, blank=True, to='login.Folder')),
                ('report_groups', models.ManyToManyField(to='login.Groups')),
                ('report_sharedwith', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SingleFileModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('single_file', models.FileField(upload_to='documents/%Y/%m/%d')),
                ('file_report', models.ForeignKey(related_name='report_files', to='login.ReportModel')),
            ],
        ),
        migrations.CreateModel(
            name='UserAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('is_site_manager', models.BooleanField(default=False)),
                ('user_name', models.CharField(max_length=100)),
                ('publicKey', models.CharField(max_length=10000)),
                ('groups', models.ManyToManyField(to='login.Groups')),
            ],
        ),
    ]
