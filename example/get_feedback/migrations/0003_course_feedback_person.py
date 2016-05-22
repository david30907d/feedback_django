# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_feedback', '0002_auto_20160519_0326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course_feedback_Person',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('Useremail', models.CharField(max_length=30)),
                ('create', models.DateTimeField()),
                ('Course_of_Feedback', models.ForeignKey(to='get_feedback.Course')),
            ],
        ),
    ]
