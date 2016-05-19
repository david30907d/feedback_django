# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='feedback_amount',
            field=models.DecimalField(default=0, decimal_places=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='course',
            name='feedback_FU',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='feedback_GPA',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='feedback_easy',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='feedback_freedom',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='feedback_knowledgeable',
            field=models.FloatField(),
        ),
    ]
