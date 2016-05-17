# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_topic', '0004_course_feedback_amount'),
    ]

    operations = [
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
