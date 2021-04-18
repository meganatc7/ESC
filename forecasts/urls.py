from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'forecasts'
urlpatterns = [
    path('detail/', views.detail, name='detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
