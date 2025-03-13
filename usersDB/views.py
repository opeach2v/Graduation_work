from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pymongo
from .models import testData

# MongoDB 연결
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["usersDB"]  # 사용할 데이터베이스
collection = db["testData"]   # 사용할 컬렉션

# DB 테스트 페이지 렌더링
def dbtest(request):
    return render(request, 'db_test.html')

@csrf_exempt
def add_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_entry = testData.objects.create(
            name=data.get("name"),
            ID=data.get("ID")
        )
        return JsonResponse({"message": "Data added successfully", "id": new_entry.id})

    # GET 요청이 들어왔을 때의 응답 추가
    return JsonResponse({"error": "GET method is not allowed for this endpoint"}, status=405)


@csrf_exempt
def get_data(request):
    if request.method == "GET":
        data = list(testData.objects.values())  # 모든 데이터를 JSON 형식으로 변환
        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "Only GET method is allowed"}, status=405)


@csrf_exempt
def delete_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            entry = testData.objects.get(id=data.get("id"))
            entry.delete()
            return JsonResponse({"message": "Data deleted successfully"})
        except testData.DoesNotExist:
            return JsonResponse({"error": "Data not found"}, status=404)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)