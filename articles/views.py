from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods, require_POST
from .forms import ArticleForm, PhotoFormSet, CommentForm, PhotoForm
from .models import Article, Photo, Comment
from forecasts import views as fore_views
import requests, json, datetime

# Create your views here.
@require_safe
def index(request):
    # 날씨 정보 ###########################################################################
    # 로그인 되어 있을 경우에만 실행
    weather_info = {}
    if request.user.is_authenticated:
        add2xy = fore_views.add2xy
        server_serviceKey = '3urgccFNfwIp7ePyvIBfqtDLrK7Sxy2YZkHZ4lc33Cf%2F242KukfpnMSZ8wPOQCh716qplOd0Pp3AtewChHHfrg%3D%3D'
        
        user_address = request.user.address[:2]
        user_nx, user_ny = add2xy.get(user_address, add2xy['서울'])

        now_date, now_hour = fore_views.time_setting()
        ultra_srt_ncst_url = f'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?serviceKey={server_serviceKey}&numOfRows=10&pageNo=1&dataType=JSON&base_date={now_date}&base_time={now_hour}&nx={user_nx}&ny={user_ny}'

        ncst_response = requests.get(ultra_srt_ncst_url)

        ncst_data_dict = ncst_response.json()  # 딕셔너리 자료형
        c_PTY = ncst_data_dict['response']['body']['items']['item'][0]['obsrValue']
        if c_PTY == '0':
            c_PTY = '비가 오지 않습니다.'
        elif c_PTY == '1':
            c_PTY = '비가 옵니다.'
        elif c_PTY == '3':
            c_PTY = '눈이 옵니다...ㅜ'
        else:
            c_PTY = '비 또는 눈이 약하게 떨어지고 있습니다.'

        c_T1H = ncst_data_dict['response']['body']['items']['item'][3]['obsrValue']

        weather_info = {
            'c_TIME': now_hour[:2] + ':' + now_hour[2:],
            'c_T1H': c_T1H,
            'c_PTY': c_PTY,
            'user_address': user_address,
        }
    
    # 게시글 ###########################################################################
    articles = Article.objects.order_by('-pk')
    context = {
        'weather_info': weather_info,
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        photo_formset = PhotoFormSet(request.POST, request.FILES)
        if article_form.is_valid() and photo_formset.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            # transaction : 여러개의 프로세스가 묶여져 하나처럼 동작
            # from django.db import transaction
            with transaction.atomic():
                article.save()
                photo_formset.instance = article
                photo_formset.save()
                return redirect('articles:index')
    else:
        article_form = ArticleForm()
        photo_formset = PhotoFormSet()
    context = {
        'article_form': article_form,
        'photo_formset': photo_formset,
    }
    return render(request, 'articles/create.html', context)


@require_safe
def detail(request, article_pk):
    # 게시물, 사진
    article = get_object_or_404(Article, pk=article_pk)
    photos = Photo.objects.filter(article_id=article_pk).all()
    # 댓글
    comment_form = CommentForm()
    comments = article.comment_set.order_by('-pk')
    context = {
        'article': article,
        'photos': photos,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    photos = list(Photo.objects.filter(article_id=article_pk).all())
    if request.method == 'POST':   
        article_form = ArticleForm(request.POST, instance=article)  
        if len(photos) > 0:      
            for photo in photos:            
                photo_form = PhotoForm(request.POST, request.FILES, instance=photo)
                if photo_form.is_valid():
                    photo_form.save()
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
        photo_form = []
        for photo in photos:
            photo_form.append(PhotoForm(instance=photo))
    context = {
        'article_form': article_form,
        'photo_form': photo_form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)


@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    photos = Photo.objects.filter(article_id=article_pk).all()
    if request.user.is_authenticated:
        if request.user == article.user:
            photos.delete()
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)

    
# 댓글 작성
@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('articles:detail', article.pk)
        context = {
            'comment_form': comment_form,
            'article': article,
        }
        return render(request, 'articles/detail.html', context)
    return redirect('accounts:login')


# 댓글 삭제
@require_POST
def comment_delete(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == article.user:
            comment.delete()
    return redirect('articles:detail', article.pk)

      
# 게시글 좋아요
@require_POST
def like(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect('articles:detail', article.pk)
    return redirect('accounts:login')


@require_safe
def board(request, category):
    articles = Article.objects.order_by('-pk')
    category = category
    likes = Article.objects.order_by('-like_users')[:3]
    context = {
        'articles': articles,
        'category': category,
        'likes': likes,
    }
    return render(request, 'articles/board.html', context)