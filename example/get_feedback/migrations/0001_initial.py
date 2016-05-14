# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('school', models.CharField(max_length=10)),
                ('courseID', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=15)),
                ('professor', models.CharField(max_length=10)),
                ('book', models.CharField(max_length=50)),
                ('feedback_freedom', models.DecimalField(decimal_places=0, max_digits=1)),
                ('feedback_FU', models.DecimalField(decimal_places=0, max_digits=1)),
                ('feedback_easy', models.DecimalField(decimal_places=0, max_digits=1)),
                ('feedback_GPA', models.DecimalField(decimal_places=0, max_digits=1)),
                ('feedback_knowledgeable', models.DecimalField(decimal_places=0, max_digits=1)),
                ('create', models.DateTimeField()),
            ],
        ),
    ]
