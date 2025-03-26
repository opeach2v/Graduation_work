from django.shortcuts import render
from django.http import HttpResponse
from .models import db_collections

def index(request):
    return HttpResponse("<h1>App is running</h1>")

def add_users(request):
    records = {
        "username": "hong2",
        "password": "hong1234",
        "role": "teacher",
        "name": "홍길동"
    }
    db_collections.insert_one(records)
    return HttpResponse("New users added")

def show_users(request):
    db = db_collection.find()
    return (db)