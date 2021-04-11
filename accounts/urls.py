from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # 회원가입
    path('signup/', views.signup, name='signup'),
    # 로그인
    path('login/', views.login, name='login'),
    # 로그아웃
    path('logout/', views.logout, name='logout'),
    # 정보수정
    path('update/', views.update, name='update'),
    # 삭제
    path('delete/', views.delete, name='delete'),
    # 이메일 인증
    path('<str:email>/signin/', views.signin, name='signin'),
]
