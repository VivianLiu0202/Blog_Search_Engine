from django.shortcuts import render, redirect,reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

from .models import BlogIndex, SearchQueryLog
from elasticsearch_dsl import Search
from datetime import datetime
import os
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver


# 用户注册视图
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登录新创建的用户
            return redirect(reverse('search'))  # 重定向到主页
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

#用户登录视图
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('search'))  # 使用 reverse 获取 search 视图的 URL
            else:
                # 在这里处理无效登录
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Create your views here.
# 站内查询
def standard_search(query):
    s = Search(index='blog').query("multi_match", query=query, fields=['title', 'content', 'author', 'abstract'])
    return s.execute()

# 短语查询
def phrase_search(query):
    s = Search(index='blog').query("match_phrase", content=query)
    return s.execute()


# 通配符查询
def wildcard_search(query):
    s = Search(index='blog').query("wildcard", content=query)
    return s.execute()


def search(request):
    query = request.GET.get('q', '')
    query_type = request.GET.get('type', 'standard')  # 默认为标准查询

    if query:
        if query_type == 'phrase':
            results = phrase_search(query)
        elif query_type == 'wildcard':
            results = wildcard_search(query)
        else:
            # 默认为标准查询
            results = standard_search(query)
    else:
        results = []
    if request.user.is_authenticated:
        SearchQueryLog.objects.create(user=request.user, query=query)
    else:
        SearchQueryLog.objects.create(query=query)

    return render(request, 'search.html', {'query_type': query_type, 'query': query, 'results': results})

@csrf_exempt
def take_snapshot(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        # 使用当前时间戳生成快照文件名
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'snapshot_{timestamp}.png'
        snapshots_folder = '/Users/liuvivian/Blog_Search_Engine/snapshots'
        snapshot_path = os.path.join(snapshots_folder, filename)

        # 用selenium生成快照
        driver = webdriver.Chrome()
        driver.get(url)
        driver.save_screenshot(snapshot_path)
        driver.quit()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required  # 可以选择只允许登录用户访问查询日志
def view_search_logs(request):
    # 获取所有日志条目或根据特定用户筛选
    if request.user.is_superuser:  # 可能只允许管理员查看所有日志
        logs = SearchQueryLog.objects.all().order_by('-timestamp')  # 最新的日志条目在前
    else:
        logs = SearchQueryLog.objects.filter(user=request.user).order_by('-timestamp')

    return render(request, 'search_logs.html', {'logs': logs})