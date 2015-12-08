# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postman', '0007_auto_20151202_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='encd',
            field=models.BooleanField(verbose_name='encrypted', default=False),
        ),
    ]
