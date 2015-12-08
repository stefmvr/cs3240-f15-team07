# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postman', '0006_auto_20151202_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='skk',
            field=models.BinaryField(default=b''),
        ),
        migrations.AlterField(
            model_name='message',
            name='symky',
            field=models.CharField(verbose_name='symkey', max_length=10000, default=''),
        ),
    ]
