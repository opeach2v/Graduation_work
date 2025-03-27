from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import users_collection

# 로그인 페이지 (메인)
def main(request):
    return render(request,'graduation_work/main.html')

# 회원가입
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
            return JsonResponse({"signup error" : str(e)}, status=500)

     # GET 요청이 들어오면 회원가입 페이지를 렌더링
    return render(request, 'graduation_work/createId_page.html')

# 로그인 처리
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            # POST 데이터 받기
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role')

            # 데이터 조회 (username, password가 일치하는 데이터가 있는지 확인)
            user_data = users_collection.find_one({"username": username, "password": password, "role": role})
            print(f"user_data: {user_data}")  # Debugging
            if user_data:
                # 세션에 사용자 정보 수동으로 저장
                request.session['username'] = user_data.get("username", [""])[0]
                request.session['password'] = user_data.get("password", [""])[0]
                request.session['role'] = user_data.get("role", [""])[0]

                if user is not None:
                    # role에 따라 리디렉션
                    if role == "parent":    # 부모님
                        return redirect('parents_page')
                    elif role == "teacher": # 선생님
                        return redirect('teachers_page')
                    else:
                        # 로그인 실패
                        return render(request, 'graduation_work/main.html', {'error': '학부모와 선생님을 다시 골라주세요.'})
                else:
                    # 로그인 실패
                    return render(request, 'graduation_work/main.html', {'error': '유저를 찾을 수 없습니다.'})
            else:
                # 로그인 실패
                return render(request, 'graduation_work/main.html', {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'})

        except Exception as e:
            return render(request, 'graduation_work/main.html', {'error': f"로그인 중 오류가 발생했습니다: {str(e)}"})
    # return render(request, 'graduation_work/main.html')

def parentsPage(request):
    return render(request, 'graduation_work/parents_page.html')

def teachersPage(request):
    return render(request, 'graduation_work/teachers_page.html')

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