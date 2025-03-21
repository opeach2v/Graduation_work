from django.shortcuts import render

def main(request):
    return render(request,'main.html')

def dbtest(request):
    return render(request, 'db_test.html')

def parentsPage(request):
    return render(request, 'parents_page.html')

def teachersPage(request):
    return render(request, 'teachers_page.html')
