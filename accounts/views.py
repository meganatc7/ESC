from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
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
