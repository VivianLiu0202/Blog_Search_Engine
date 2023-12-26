# search/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),# 注意这里是空字符串，代表 search/ 应用的根路径
]

