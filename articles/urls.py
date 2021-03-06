from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    # 댓글 작성
    path('<int:article_pk>/comment', views.comment_create, name='comment_create'),
    # 댓글 수정
    path('<int:article_pk>/<int:comment_pk>/update', views.comment_update, name='comment_update'),
    # 댓글 삭제
    path('<int:article_pk>/<int:comment_pk>/delete', views.comment_delete, name='comment_delete'),
    # 게시글 좋아요
    path('<int:article_pk>/like/', views.like, name='like'),
    # 게시판
    path('board/<int:category>/', views.board, name='board'),
    # 게시물 검색
    path('search/', views.search, name='search'),
]
