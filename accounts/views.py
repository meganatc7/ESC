from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from .models import User
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Create your views here.
# 가입 유저에게 이메일 보내는 함수
def send_email(email):
    url = f'http://127.0.0.1:8000/accounts/{email}/signin'
    send_mail(
        '이메일 인증을 해주세요',
        f'해당 주소로 이동해주세요 {url}', # 해당 url클릭 시 signin으로
        'meganatc7@gmail.com',
        [f'{email}'],
    )


@require_safe
def signin(request, email):
    # 해당 유저 객체를 받아온 뒤 is_active값을 1로 바꿔줌
    user = get_object_or_404(User, email=email)
    user.is_active = 1
    user.save()
    auth_login(request, user)
    return redirect('accounts:login')


@require_http_methods(['GET','POST'])
def signup(request):
    # 로그인 되어있는 경우 인덱스 페이지로
    if request.user.is_authenticated:
        return redirect('articles:index')

    # POST 요청
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        # 유효성 검사
        if form.is_valid():
            user = form.save()
            # 유효성 검사 하고 난 뒤 이메일 보내기
            send_email(user.email)
            print('이메일 발송')
            # return JsonResponse({'messgae': 'works'})
            return redirect('articles:index')
    # GET 요청
    else:
        form = CustomUserCreationForm()
    print('에러',form.errors)
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET','POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    # POST 요청인 경우 유효성 검사한 뒤 로그인
    if request.method == 'POST': 
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
    # GET 요청인 경우 로그인 페이지로
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def cropped(request):
    print('확인',request)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_http_methods(['GET','POST'])
def update(request):
    # POST 요청인 경우
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    # GET 요청인 경우
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def delete(request):
    request.user.delete()
    update_session_auth_hash(request, request.user)
    return redirect('articles:index')


def profile(request, nickname):
    person = get_object_or_404(get_user_model(), nickname=nickname)
    form = CustomUserChangeForm()
    context = {
        'person': person,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)