from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'), # 회원가입
    path('login/', views.login, name='login'), # 로그인
]
