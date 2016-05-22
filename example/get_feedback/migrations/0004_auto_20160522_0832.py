# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_feedback', '0003_course_feedback_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseFeedbackPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('Useremail', models.CharField(max_length=30)),
                ('create', models.DateTimeField()),
                ('Course_of_Feedback', models.ForeignKey(to='get_feedback.Course')),
            ],
        ),
        migrations.RemoveField(
            model_name='course_feedback_person',
            name='Course_of_Feedback',
        ),
        migrations.DeleteModel(
            name='Course_feedback_Person',
        ),
    ]
