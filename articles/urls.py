from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
    # 댓글 작성
    path('<int:article_pk>/comment', views.comment_create, name='comment_create'),
]
