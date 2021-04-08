from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, PhotoFormSet, CommentForm
from .models import Article, Photo, Comment

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
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
    comments = article.comment_set.order_by('-pk')
    context = {
        'article': article,
        'photos': photos,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


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