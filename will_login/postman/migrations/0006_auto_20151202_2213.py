# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postman', '0005_auto_20151202_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='skk',
            field=models.BinaryField(default=b''),
            preserve_default=False,
        ),

    ]
