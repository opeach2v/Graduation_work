from django.db import models
from db_connect import db

users_collection = db['users']

class FileUploads(models.Model):
    title = models.CharField(max_length = 200)
    uploadedFile = models.FileField(upload_to = "uploads/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)