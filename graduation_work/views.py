from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .models import users_collection

# 로그인 페이지 (메인)
def main(request):
    return render(request,'graduation_work/main.html')

# 회원가입 처리
@csrf_exempt
def add_users(request):
    if request.method == 'POST':
        try:
            # POST 데이터 받기
            username = request.POST.get('username'),
            password = request.POST.get('password'),
            role = request.POST.get('role'),
            name = request.POST.get('name'),

            # 데이터 생성
            data = {
                "username": username,
                "password": password,
                "role": role,
                "name": name,
                "createdAt": datetime.now()
            }

            # mongoDB에 저장
            users_collection.insert_one(data)
        except Exception as e:
            return JsonResponse({"error" : str(e)}, status=500)

     # GET 요청이 들어오면 회원가입 페이지를 렌더링
    return render(request, 'graduation_work/createId_page.html')


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