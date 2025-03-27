from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='login'),
    path('signup/', views.add_users, name='add_users'),    # 회원가입 처리
    path('show/', views.show_users),
]