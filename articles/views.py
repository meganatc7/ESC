from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, PhotoFormSet
from .models import Article, Photo

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')


def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        photo_formset = PhotoFormSet(request.POST, request.FILES)
        if article_form.is_valid() and photo_formset.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user # [중요!]로그인 후 확인해보기!!

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