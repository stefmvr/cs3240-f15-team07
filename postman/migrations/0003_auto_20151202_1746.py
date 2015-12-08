# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postman', '0002_message_symky'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='symky',
            field=models.CharField(max_length=2048, default='', verbose_name='symkey'),
        ),
    ]
