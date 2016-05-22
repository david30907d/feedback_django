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
  feedback_amount = models.DecimalField(max_digits=10,decimal_places=0,default=0)
  feedback_freedom = models.FloatField()
  feedback_FU = models.FloatField()
  feedback_easy = models.FloatField()
  feedback_GPA = models.FloatField()
  feedback_knowledgeable = models.FloatField()
  # those five field is for feedback on spirit.
  create = models.DateTimeField()
  def __str__(self):
    return self.name
  def check_courseID_and_name_not_empty(self):
    return (self.courseID!=None and self.courseID!="") and (self.name!=None and self.name!="")

class Course_feedback_Person(models.Model):
  # 這是有參與心得抽獎的人
  Course_of_Feedback = models.ForeignKey(Course)
  Useremail = models.CharField(max_length=30) 
  create = models.DateTimeField()
  def __str__(self):
    return self.Useremail