from django.urls import path
from . import views

app_name = 'forecasts'
urlpatterns = [
    path('', views.index, name='index'),
]
