# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_topic', '0005_auto_20160517_1209'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Course',
        ),
    ]
