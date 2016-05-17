# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_topic', '0003_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='feedback_amount',
            field=models.DecimalField(default=0, decimal_places=0, max_digits=10),
        ),
    ]
