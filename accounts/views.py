from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from .models import User
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib import messages
import json
import string, random

# Create your views here.
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# 가입 유저에게 이메일 보내는 함수
def send_email(email):
    url = f'http://127.0.0.1:8000/accounts/{email}/signin'
    html_content = render_to_string('accounts/email_template.html', {
        'title': 'test email',
        'url': url,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        #subject
        'ESC 이메일 인증',
        #content
        text_content,
        #from email
        settings.EMAIL_HOST_USER,
        #to
        [email],
    )

    email.attach_alternative(html_content,'text/html')
    email.send()


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
            user = form.save(commit=False)
            print(request.POST.get('cropped'))
            user.image = request.POST.get('cropped')
            user.save()
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
        else:
            messages.add_message(request, messages.WARNING, '아이디 혹은 비밀번호가 틀렸습니다.')
    # GET 요청인 경우 로그인 페이지로
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def cropped(request):
    print('확인',request.POST, request.FILES)
    cropped = request.FILES.get('file')
    # print(cropped)
    path = default_storage.save(f'profile/{cropped.name}', cropped)
    return JsonResponse({'path':path})


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


@require_POST
def updateprofile(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        user.image = request.FILES.get('file')
        user.save()
        return JsonResponse({'message':'works'})


@login_required
def delete(request):
    request.user.delete()
    update_session_auth_hash(request, request.user)
    return redirect('articles:index')


@require_safe
def profile(request, nickname):
    person = get_object_or_404(get_user_model(), nickname=nickname)
    articles = person.article_set.all()
    form = CustomUserChangeForm()
    context = {
        'person': person,
        'form': form,
        'articles': articles,
    }
    return render(request, 'accounts/profile.html', context)


@require_http_methods(['GET','POST'])
def changepw(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Success!!')
            return redirect('accounts:profile', user.nickname)
        else:
            messages.error(request, 'Failed!!')
    form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password.html', context)


@require_http_methods(['GET','POST'])
def findpw(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        target_user = User.objects.get(email=email)
        print(target_user.username)
        if target_user:
            # 임의의 인증번호 생성
            string_pool = string.ascii_letters + string.digits
            auth_num = ""
            for _ in range(8):
                auth_num += random.choice(string_pool)
            
            target_user.auth = auth_num
            target_user.save()

            send_mail(
                '비밀번호 찾기 인증메일입니다.',
                f'인증번호: {auth_num}',
                'meganatc7@gmail.com',
                [email],
            )
        return JsonResponse({'result': target_user.username})
    else:
        form = CustomPasswordResetForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/findpassword.html', context)


def authpw(request):
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    target_user = User.objects.get(username=user_id, auth=input_auth_num)
    target_user.auth = ""
    target_user.save()
    request.session['auth'] = target_user.username

    return JsonResponse({'result': target_user.username})


@require_http_methods(['GET','POST'])
def resetpw(request):
    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = User.objects.get(username=session_user)
        auth_login(request, current_user)

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)

        if reset_password_form.is_valid():
            user = reset_password_form.save()
            messages.success(request, '비밀번호 변경 완료!')
            auth_logout(request)
            return redirect('accounts:login')
        else:
            auth_logout(request)
            # request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)
    context = {
        'form': reset_password_form,
    }
    return render(request, 'accounts/password_reset.html', context)