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
    # 비밀번호 변경
    path('change_password/', views.changepw, name='changepw'),
    # 비밀번호 찾기
    path('find_password/', views.findpw, name='findpw'),
    path('pw/auth/', views.authpw, name='authpw'),
    path('pw/reset/', views.resetpw, name='resetpw'),
]
