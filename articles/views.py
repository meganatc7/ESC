from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, PhotoFormSet, CommentForm
from .models import Article, Photo, Comment
from django.core.paginator import Paginator
from forecasts import views as fore_views
import requests, json, datetime
from django.http import JsonResponse

# Create your views here.
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
    articles = Article.objects.order_by('-created_at')
    # articles 테이블의 모든 레코드를 페이지네이터에 5개씩 저장
    paginator = Paginator(articles, 5)
    # request된 page 저장
    page = request.GET.get('page')
    # request된 page의 레코드 저장
    posts = paginator.get_page(page)
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


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


def detail(request, article_pk):
    # 게시물, 사진
    article = get_object_or_404(Article, pk=article_pk)
    photos = Photo.objects.filter(article_id=article_pk).all()
    # 댓글
    comment_form = CommentForm()
    comments = article.comment_set.order_by('-created_at')
    context = {
        'article': article,
        'photos': photos,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
                article_form.save()
                return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)


# 댓글 작성
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


# 댓글 수정
@login_required
@require_http_methods(['GET', 'POST'])
def comment_update(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        comment_update_form = CommentForm(request.POST, instance=comment)
        if comment_update_form.is_valid():
            comment_update_form.save()
            return redirect('articles:detail', article.pk)
    else:
        comment_update_form = CommentForm(instance=comment)
    context = {
        'article': article,
        'comment': comment,
        'comment_update_form': comment_update_form,
    }
    return render(request, 'articles/detail.html', context)


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
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user.is_authenticated:
        like = 0
        article = get_object_or_404(Article, pk=article_pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
            like = 0
            like_number = article.like_users.all().count()
        else:
            article.like_users.add(request.user)
            like_number = article.like_users.all().count()
            like = 1
        return JsonResponse({'message':'works', 'like': like, 'like_number': like_number})
    return redirect('accounts:login')


@require_safe
def board(request, category):
    articles = Article.objects.filter(category=category).order_by('-created_at')
    likes = Article.objects.order_by('-like_users')[:3]
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        'articles': articles,
        'likes': likes,
        'posts': posts,
    }
    return render(request, 'articles/board.html', context)


@require_POST
def search(request):
    articles = Article.objects.order_by("-created_at")
    search = request.POST.get('search')
    search_articles = []
    for article in articles:
        if search in article.title:
            search_articles.append(article)
    context = {
        'articles': articles,
        'search': search,
        'search_articles': search_articles,
    }
    return render(request, 'articles/search.html', context)
