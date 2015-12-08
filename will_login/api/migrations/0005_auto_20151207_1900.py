# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20151123_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='report2_api',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('file_name', models.FileField(upload_to='')),
            ],
            options={
                'ordering': ('file_name',),
            },
        ),
        migrations.CreateModel(
            name='report_api',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('report_title', models.TextField()),
                ('report_body', models.TextField()),
                ('id_num', models.TextField()),
            ],
            options={
                'ordering': ('report_title',),
            },
        ),
        migrations.AlterModelOptions(
            name='api',
            options={'ordering': ('username',)},
        ),
        migrations.RemoveField(
            model_name='api',
            name='access',
        ),
        migrations.RemoveField(
            model_name='api',
            name='created',
        ),
    ]
