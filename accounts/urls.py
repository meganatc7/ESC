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
    # 프로필 수정
    path('update/profile/', views.updateprofile, name='updateprofile'),
    # 삭제
    path('delete/', views.delete, name='delete'),
    # 이메일 인증
    path('<str:email>/signin/', views.signin, name='signin'),
    # 프로필 페이지
    path('<str:nickname>/profile/', views.profile, name='profile'),
    # crop사진 임시 저장
    path('cropped/', views.cropped, name='cropped'),
]
