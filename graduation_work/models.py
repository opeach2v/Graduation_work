from django.db import models
from db_connect import db

users_collection = db['users']
results_collection = db['ai_results']

class FileUploads(models.Model):
    title = models.CharField(max_length = 200)
    uploadedFile = models.FileField(upload_to = "uploads/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)