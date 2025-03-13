from django.shortcuts import render

def main(request):
    return render(request,'login_page.html')

def dbtest(request):
    return render(request, 'db_test.html')

