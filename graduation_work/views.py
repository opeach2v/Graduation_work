from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from .models import users_collection, results_collection
from . import models
from django.views.decorators.cache import never_cache

import bcrypt;

# 로그인 페이지 (메인)
def main(request):
    return render(request,'graduation_work/main.html')

# 회원가입
@csrf_exempt
@never_cache
def add_users(request):
    if request.method == 'POST':
        try:
            # POST 데이터 받기
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role')
            name = request.POST.get('name')

            # TODO  username과 password가 영어일 때만 넘어가고, 무조건 4개 항목이 다 입력되어야 가입되도록 해야 함.
            # TODO  가입 되면 그냥 로그인 페이지로 가는 게 아니라 회원가입 됐다고 뜨도록 해야 함

            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8');

            # 데이터 생성
            data = {
                "username": username,
                "password": hashed_pw,  # 해시된 비번 저장
                "role": role,
                "name": name,
                "createdAt": datetime.now()
            }

            # mongoDB에 저장
            users_collection.insert_one(data)
            return redirect('login_user')  # 회원가입 후 로그인 페이지로 리다이렉션
        except Exception as e:
            return JsonResponse({"signup error" : str(e)}, status=500)

    # GET 요청이 들어오면 회원가입 페이지를 렌더링
    return render(request, 'graduation_work/createId_page.html')

# 로그인 처리
@csrf_exempt
@never_cache
def login_user(request):
    if request.method == 'POST':
        try:
            # POST 데이터 받기
            username = request.POST.get('username')
            input_password = request.POST.get('password')
            role = request.POST.get('role')

            # 데이터 조회 (username, password가 일치하는 데이터가 있는지 확인)
            user_data = users_collection.find_one({"username": username, "role": role})
            print(f"user_data: {user_data}")  # Debugging
            if user_data:
                hashed_pw = user_data.get('password');  # 문자열로 가져옴

                # 세션에 사용자 정보 수동으로 저장
                # 비밀번호 비교 (바이트로 변환)
                if bcrypt.checkpw(input_password.encode('utf-8'), hashed_pw.encode('utf-8')) :
                    request.session['username'] = user_data.get("username")
                    request.session['role'] = user_data.get("role")
                    request.session['name'] = user_data.get("name", [None])[0]
                
                    # role에 따라 리디렉션
                    if role == "parent":    # 부모님
                        return redirect('parents_page')
                    elif role == "teacher": # 선생님
                        return redirect('teachers_page')
                    else:
                        # 로그인 실패
                        return render(request, 'graduation_work/main.html', {'error': '학부모와 선생님을 다시 선택해주세요.'})
                else:
                    # 로그인 실패
                    return render(request, 'graduation_work/main.html', {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'})
            else:
                # 로그인 실패
                return render(request, 'graduation_work/main.html', {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'})

        except Exception as e:
            return render(request, 'graduation_work/main.html', {'error': f"로그인 중 오류가 발생했습니다: {str(e)}"})
    return render(request, 'graduation_work/main.html')

@never_cache
def parentsPage(request):
    # 로그인 안 햇는데도 URL로 접근하려고 하면 막음
    if not request.session.get('username'):
        return redirect('login_user')
    name = request.session.get('name')  # 세션에 저장했던 값 꺼냄

    return render(request, 'graduation_work/parents_page.html', {
        'name' : name
    })

@never_cache
def teachersPage(request):
    # 로그인 안 햇는데도 URL로 접근하려고 하면 막음
    if not request.session.get('username'):
        return redirect('login_user')
    name = request.session.get('name')


    return render(request, 'graduation_work/teachers_page.html', {
        'name' : name
    })

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

# 로그아웃
def logout_view(request) :
    request.session.flush();    # 세션 전체 삭제 (뒤로가기 되면 안 됨)
    django_logout(request)
    return redirect('login_user')


# 파일 업로드
def uplooadFile(request):
    if request.method == "POST":
        fileTitle = request.POST['fileTitle']
        uploadedFile = request.FILES["uploadedFile"]

        # DB에 저장
        fileUploads = models.FileUploads(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        fileUploads.save()

    fileUpload = models.FileUploads.objects.all()

    return render(request, "teachers_page.html", context = {
        "files": fileUpload
    })


# DB ai_results 컬렉션에 값 입력해서 넣기
def input_results(request):
    if request.method == 'POST':
        try:
            # POST 데이터 받기
            child_id = request.POST.get('child_id')
            event_type = request.POST.get('event_type')
            confidence = request.POST.get('confidence')
            timestamp = request.POST.get('timestamp')

            # 데이터 생성
            data = {
                "child_id": child_id,
                "event_type": event_type,
                "confidence": confidence,
                "timestamp": timestamp
            }

            # mongoDB에 저장
            results_collection.insert_one(data)
            return redirect('input_results')
        except Exception as e:
            return JsonResponse({"input error" : str(e)}, status=500)

    # GET 요청이 들어오면 입력창을 렌더링
    return render(request, 'graduation_work/temporary_inputResult.html')

# ai_results 값 보기
def showResults(request):
    res = []
    for doc in results_collection.find({}):
        child_id = doc.get("child_id")
        event_type = doc.get("event_type")
        confidence = doc.get("confidence")
        timestamp = doc.get("timestamp")
        res.append({"child_id": child_id, "event_type": event_type, "confidence": confidence, "timestamp": timestamp})
    
    return JsonResponse({'res': res}, safe=False, json_dumps_params={'ensure_ascii': False}, content_type="application/json; charset=UTF-8")