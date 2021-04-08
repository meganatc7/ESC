from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods, require_POST

# Create your views here.
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
            auth_login(request, user)
            return redirect('articles:index')
    # GET 요청
    else:
        form = CustomUserCreationForm()
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


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_http_methods(['GET','POST'])
def update(request):
    # POST 요청인 경우
    if request.method == 'POST':
        pass
    # GET 요청인 경우
    else:
        form = CustomUserChangeForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)