from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_http_methods, require_POST
from .forms import ArticleForm, PhotoFormSet, CommentForm
from .models import Article, Photo, Comment

# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
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