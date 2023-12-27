# search/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),# 注意这里是空字符串，代表 search/ 应用的根路径
    path('take_snapshot/', views.take_snapshot, name='snapshot'),
    path('logs/', views.view_search_logs, name='view_search_logs'),
    # 登录页面的URL
    path('login/', views.login_view, name='login'),
    # 注册页面的URL
    path('register/', views.signup_view, name='register'),
]

