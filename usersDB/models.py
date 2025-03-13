from django.db import models
from django.conf import settings

class teachers(models.Model):
    teacherID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phoneNum = models.CharField(max_length=50)
    ID = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    classNum = models.IntegerField(default=0)

class testData(models.Model):
    name = models.CharField(max_length=100)
    ID = models.CharField(max_length=50)