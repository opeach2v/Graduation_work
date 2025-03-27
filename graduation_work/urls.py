from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.main, name='login'),
    path('signup/', views.show_createId_page, name='signup_form'),  # 회원가입 페이지
    path('add/', views.add_users, name='add_users'),    # 회원가입 처리
    path('show/', views.show_users),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)