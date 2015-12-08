# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151122_1508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='api',
            old_name='code',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='api',
            old_name='title',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='api',
            name='language',
        ),
        migrations.RemoveField(
            model_name='api',
            name='linenos',
        ),
        migrations.RemoveField(
            model_name='api',
            name='style',
        ),
    ]
