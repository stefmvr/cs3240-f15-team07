# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151122_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='username',
            field=models.CharField(max_length=100, default='', blank=True),
        ),
    ]
