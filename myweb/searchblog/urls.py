# search/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # 根路径是登录视图
    path('search/', views.search, name='search'),  # 搜索表单的URL
    path('results/', views.search_results, name='search_results'),
    path('take_snapshot/', views.take_snapshot, name='snapshot'),
    path('logs/', views.view_search_logs, name='view_search_logs'),
    path('register/', views.signup_view, name='register'),  # 注册页面的URL
    path('record_click/', views.record_click, name='record_click'),
]

