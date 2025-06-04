from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import date, datetime
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from .models import users_collection, results_collection, children_collection, teachers_collection, parents_collection
from . import models
from django.views.decorators.cache import never_cache
from django.contrib import messages
import json, re
from bson import ObjectId

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
            contact = request.POST.get('phoneNumber')
            if role == "teacher":
                classroom = request.POST.get('classroom')

            # 모든 항목이 입력되었는지 확인
            if not all([username, password, role, name, contact]):
                messages.error(request, "모든 항목을 입력해주세요.")
                return redirect('add_users')  # 회원가입 페이지로 다시 이동

            # username과 password는 영어(알파벳)만 허용
            if not re.fullmatch(r'[A-Za-z]+', username) or not re.fullmatch(r'[A-Za-z]+', password):
                messages.error(request, "아이디와 비밀번호는 영문자만 사용 가능합니다.")
                return redirect('add_users')

            # 비밀번호 해싱
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8');

            # 데이터 생성
            data = {
                "username": username,
                "password": hashed_pw,  # 해시된 비번 저장
                "role": role,
                "name": name,
                "createdAt": datetime.now()
            }

            print("Saving user:", data)  # 확인용 출력

            # mongoDB users 컬렉션에 저장 저장
            users_collection.insert_one(data)

            if role == "parent":
                parents_collection.insert_one({
                    "name": name,
                    "contact": contact,
                    "children_ids": []
                })
            elif role == "teacher":
                teachers_collection.insert_one({
                    "name": name,
                    "contact": contact,
                    "classroom": classroom
                })

            # 성공 메시지와 함께 로그인 페이지로 이동
            messages.success(request, f"{name} 님, 회원가입이 완료되었습니다. 로그인 해주세요!")
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
                        parent_data = parents_collection.find_one({"children_ids": {"$ne": []}})    # 빈 리스트가 아닌 경우에만 찾음
                        # 세션에 저장 (조건: 존재하고 children_ids가 비어있지 않으면)
                        if parent_data and 'children_ids' in parent_data:
                            request.session['children_ids'] = parent_data['children_ids'];
                        else:
                            request.session['children_ids'] = []  # 기본값
                        return redirect('parents_page')
                    elif role == "teacher": # 선생님
                        teacher_data = teachers_collection.find_one({"username": username})
                        if teacher_data and 'classroom' in teacher_data:
                            request.session['classroom'] = teacher_data['classroom']
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
    children_ids = request.session.get('children_ids', [])  # 리스트 형태로 불러오기

    return render(request, 'graduation_work/parents_page.html', {
        'name' : name,
        'children_ids': children_ids
    })

@never_cache
def teachersPage(request):
    # 로그인 안 햇는데도 URL로 접근하려고 하면 막음
    if not request.session.get('username'):
        return redirect('login_user')
    name = request.session.get('name')
    classroom = request.session.get('classroom')

    return render(request, 'graduation_work/teachers_page.html', {
        'name' : name,
        'classroom': classroom
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
            event_type = request.POST.get('action')
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

# ai_results 데이터 삭제
def deleteRes(request):
    res = results_collection.delete_many({})
    return HttpResponse(f"{res.deleted_count} documents deleted from 'actions'")

# 유저 데이터 삭제
def deleteUsers(request):
    res = users_collection.delete_many({})
    return HttpResponse(f"{res.deleted_count} documents deleted from 'actions'")

# 부모님 컬렉션 값 보기
def showParents(request):
    parents = []
    for parent_doc in parents_collection.find({}):
        parent = {
            "_id": parent_doc.get("_id"),
            "name": parent_doc.get("name"),
            "contact": parent_doc.get("contact"),
            "children": []
        }

        for cid in parent_doc.get("children_ids", []):
            child = children_collection.find_one({"_id": ObjectId(cid)})
            if child:
                birthdate = child.get("birthdate")
                if birthdate and isinstance(birthdate, datetime):
                    age = calculate_age(birthdate.date())  # datetime.date로 변환
                else:
                    age = "정보 없음"

                parent["children"].append({
                    "id": str(child["_id"]),
                    "name": child["name"],
                    "age": f"{age}세" if isinstance(age, int) else age,
                })

        parents.append(parent)

    return render(request, 'graduation_work/parents_page.html', {
        "parents": parents
    })

# 만 나이 계산 함수
def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )

# 부모님 데이터 삭제
def deleteParents(request):
    res = parents_collection.delete_many({})
    return HttpResponse(f"{res.deleted_count} documents deleted from 'actions'")

# 선생님 컬렉션 값 보기
def showTeachers(request):
    res = []
    for doc in teachers_collection.find({}):
        _id = doc.get("_id")
        name = doc.get("name")
        contant = doc.get("contant")
        classroom = doc.get("classroom")
        res.append({"_id": str(_id), "name": name, "contant": contant, "classroom": classroom})
    
    return JsonResponse({'res': res}, safe=False, json_dumps_params={'ensure_ascii': False}, content_type="application/json; charset=UTF-8")

# 선생님 데이터 삭제
def deleteTeachers(request):
    res = teachers_collection.delete_many({})
    return HttpResponse(f"{res.deleted_count} documents deleted from 'actions'")

@csrf_exempt
def add_child(request):
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        child_name = request.POST.get('childname')
        birthdate = request.POST.get('birthdate')
        classroom = request.POST.get('classroom')

        format_birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
        # 데이터 생성
        data = {
            "name": child_name,
            "birthdate": format_birthdate,
            "parent_id": parent_id,
            "classroom": classroom
        }

        # mongoDB에 어린이 데이터 저장
        inserted_child = children_collection.insert_one(data)

        child_id = inserted_child.inserted_id   # 자녀의 _id 가져오기

        # 그리고 생성된 어린이 고유 id를 부모님 컬렉션에 업데이트
        parents_collection.update_one(
            {"_id": ObjectId(parent_id)},
            {"$push": {"children_ids": child_id}}  # child_id
        )
        return redirect('parents_page')  # 다시 부모 페이지로