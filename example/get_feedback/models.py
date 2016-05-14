from django.db import models
from datetime import datetime
# Create your models here.
class Course(models.Model):
  school = models.CharField(max_length=10)
  courseID = models.CharField(max_length=15)
  name = models.CharField(max_length=15)
  professor = models.CharField(max_length=10)
  book = models.CharField(max_length=50)
  # those five field is for feedback on spirit.
  feedback_freedom = models.DecimalField(max_digits=1, decimal_places=0)
  feedback_FU = models.DecimalField(max_digits=1, decimal_places=0)
  feedback_easy = models.DecimalField(max_digits=1, decimal_places=0)
  feedback_GPA = models.DecimalField(max_digits=1, decimal_places=0)
  feedback_knowledgeable = models.DecimalField(max_digits=1, decimal_places=0)
  # those five field is for feedback on spirit.
  create = models.DateTimeField()
  def __str__(self):
    return self.name
  def check_courseID_and_name_not_empty(self):
    return (self.courseID!=None and self.courseID!="") and (self.name!=None and self.name!="")