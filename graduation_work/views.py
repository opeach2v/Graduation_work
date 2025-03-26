from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import db_collection

def index(request):
    return HttpResponse("<h1>App is running</h1>")

def add_users(request):
    data = {
        "username": "jang",
        "password": "jang1234",
        "role": "parent",
        "name": "장혜진"
    }

    db_collection.insert_one(data)
    return JsonResponse({"message" : "Data saved successfully"})

def show_users(request):
    users = []
    for doc in db_collection.find({}):
        username = doc.get("username")
        password = doc.get("password")
        role = doc.get("role")
        name = doc.get("name")
        users.append({"username": username, "password": password, "role": role, "name": name})
    
    return JsonResponse({'users': users}, safe=False, json_dumps_params={'ensure_ascii': False}, content_type="application/json; charset=UTF-8")