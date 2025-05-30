from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),    # 메인 페이지(로그인 페이지)
    path('login/', views.login_user, name='login_user'),    # 로그인 페이지
    path('signup/', views.add_users, name='add_users'),    # 회원가입 페이지 및 회원가입 처리
    path('parents/', views.parentsPage, name='parents_page'),    # 부모님 페이지
    path('teachers/', views.teachersPage, name='teachers_page'),    # 선생님 페이지
    path('logout/', views.logout_view, name='logout'),
    path('show/', views.show_users),
    path('res_show/', views.showResults),
    path('addresult/', views.input_results, name='input_results'),  # 임시로 만든 거
]