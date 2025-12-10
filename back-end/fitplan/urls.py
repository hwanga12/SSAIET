# fitplan/urls.py

from django.urls import path
from . import views

app_name = 'fitplan'
urlpatterns = [
    path('', views.index, name='index'),  # 기본 페이지를 설정
]