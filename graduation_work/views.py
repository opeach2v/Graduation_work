from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import users_collection

def index(request):
    return HttpResponse("<h1>App is running</h1>")

def add_users(request):
    try:
        data = {
        "username": "jang",
        "password": "jang1234",
        "role": "parent",
        "name": "장혜진",
        "createdAt": datetime.now()
        }

        users_collection.insert_one(data)
        return JsonResponse({"message" : "Data saved successfully"})

    except Exception as e:
        return JsonResponse({"error" : str(e)}, status=500)

def show_users(request):
    users = []
    for doc in users_collection.find({}):
        username = doc.get("username")
        password = doc.get("password")
        role = doc.get("role")
        name = doc.get("name")
        createdAt = doc.get("createdAt")
        users.append({"username": username, "password": password, "role": role, "name": name, "createdAt": createdAt})
    
    return JsonResponse({'users': users}, safe=False, json_dumps_params={'ensure_ascii': False}, content_type="application/json; charset=UTF-8")