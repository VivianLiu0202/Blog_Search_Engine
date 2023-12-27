from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator

from .models import BlogIndex, SearchQueryLog, ClickLog
from elasticsearch_dsl import Search,Q
from elasticsearch_dsl.query import FunctionScore
from datetime import datetime
import os
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO

from collections import Counter
import jieba  # 使用jieba分词库进行中文分词


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
def standard_search(query, user=None, size=10000, sort_by='pagerank_only'):
    # 基础查询
    base_query = Q("multi_match", query=query, fields=['title', 'content','author','abstract'])

    # 如果选择个性化排序并且用户已登录
    if sort_by == 'personalize_search' and user is not None:
        user_profile = {
            'favorite_field': user.favorite_field,
            'occupation': user.occupation
        }
        top_queries = get_top_queries(user)
        print(top_queries)

        # 构建函数评分查询
        functions = []
        if user_profile['favorite_field']:
            functions.append({"filter": Q("term", content=user_profile['favorite_field']), "weight": 2})
        if user_profile['occupation']:
            functions.append({"filter": Q("term", content=user_profile['occupation']), "weight": 2})
        for word in top_queries:
            functions.append({"filter": Q("term", content=word), "weight": 1.5})

        function_score_query = Q(FunctionScore(query=base_query, functions=functions, boost_mode="sum"))
        s = Search(index='blog').query(function_score_query)
        s = s.sort({'_score': {'order': 'desc'}}, {'PR': {'order': 'desc'}})

    # 如果选择PR排序或用户未登录
    else:
        s = Search(index='blog').query(base_query)
        s = s.sort({'PR': {'order': 'desc'}})

    s = s[:size]
    response = s.execute()
    return list(response)


# 短语查询
def phrase_search(query, user=None, size=10000, sort_by='pagerank_only'):
    base_query = Q("match_phrase", content=query)
    # 如果选择了个性化搜索并且用户已登录
    if sort_by == 'personalize_search' and user is not None:
        user_profile = {
            'favorite_field': user.favorite_field,
            'occupation': user.occupation
        }
        top_queries = get_top_queries(user)

        functions = []
        if user_profile['favorite_field']:
            functions.append({"filter": Q("term", content=user_profile['favorite_field']), "weight": 2})
        if user_profile['occupation']:
            functions.append({"filter": Q("term", content=user_profile['occupation']), "weight": 2})
        for word in top_queries:
            functions.append({"filter": Q("term", content=word), "weight": 1.5})

        function_score_query = Q(FunctionScore(query=base_query, functions=functions, boost_mode="sum"))
        s = Search(index='blog').query(function_score_query)
        s = s.sort({'_score': {'order': 'desc'}}, {'PR': {'order': 'desc'}})
    else:
        s = Search(index='blog').query(base_query)
        s = s.sort({'PR': {'order': 'desc'}})
    response = s.execute()
    return list(response)

# 通配符查询
def wildcard_search(query,user=None, size=10000, sort_by='pagerank_only'):
    base_query = Q("wildcard", title=query)
    # 如果选择了个性化搜索并且用户已登录
    if sort_by == 'personalize_search' and user is not None:
        user_profile = {
            'favorite_field': user.favorite_field,
            'occupation': user.occupation
        }
        top_queries = get_top_queries(user)

        functions = []
        if user_profile['favorite_field']:
            functions.append({"filter": Q("term", content=user_profile['favorite_field']), "weight": 2})
        if user_profile['occupation']:
            functions.append({"filter": Q("term", content=user_profile['occupation']), "weight": 2})
        for word in top_queries:
            functions.append({"filter": Q("term", content=word), "weight": 1.5})

        function_score_query = Q(FunctionScore(query=base_query, functions=functions, boost_mode="sum"))
        s = Search(index='blog').query(function_score_query)
        s = s.sort({'_score': {'order': 'desc'}}, {'PR': {'order': 'desc'}})
    else:
        s = Search(index='blog').query(base_query)
        s = s.sort({'PR': {'order': 'desc'}})
    response = s.execute()
    return list(response)

def search(request):
    # 只渲染搜索表单并等待用户输入
    return render(request, 'search.html')

# 搜索结果
def search_results(request):
    query = request.GET.get('q', '')
    query_type = request.GET.get('type', 'standard')
    sort_method = request.GET.get('sort_method', 'pagerank_only')
    print(sort_method)
    user = request.user if request.user.is_authenticated else None
    results = []
        
    if query:
        # 添加一个参数记录查询的方式
        if request.user.is_authenticated:
            if query_type == 'phrase':
                results = phrase_search(query, user=user, size=10000, sort_by=sort_method)
            elif query_type == 'wildcard':
                results = wildcard_search(query, user=user, size=10000, sort_by=sort_method)
            else:
                results = standard_search(query, user=user, size=10000, sort_by=sort_method)
        else:
            # 对于未登录用户，可能需要使用不同的逻辑或默认到标准查询
            results = standard_search(query,user=None,size=10000, sort_by=sort_method)

        # 如果用户已登录，记录搜索查询日志
        if request.user.is_authenticated:
            SearchQueryLog.objects.create(user=request.user, query=query)
        else:
            SearchQueryLog.objects.create(query=query)

        # 分页处理
        paginator = Paginator(results, 30)  # 每页显示30个结果
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # 渲染到结果模板
        return render(request, 'results.html', {
            'query_type': query_type,
            'query': query,
            'sort_method': sort_method,  # 这行确保sort_method被传回模板
            'page_obj': page_obj,
        })

    # 如果没有查询参数，重定向回主搜索页面
    return redirect('search')

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

def get_top_queries(user):
    logs = SearchQueryLog.objects.filter(user=user)
    queries = logs.values_list('query', flat=True)
    word_count = Counter()
    for query in queries:
        words = jieba.cut(query)
        word_count.update(words)
    most_common_words = [word for word, count in word_count.most_common(10)]
    return most_common_words


@login_required
def view_search_logs(request):
    # 获取所有日志条目或根据特定用户筛选
    if request.user.is_superuser:
        logs = SearchQueryLog.objects.all().order_by('-timestamp')
        click_logs = ClickLog.objects.all().order_by('-timestamp')
    else:
        logs = SearchQueryLog.objects.filter(user=request.user).order_by('-timestamp')
        click_logs = ClickLog.objects.filter(user=request.user).order_by('-timestamp')

    # 计算最常搜索的关键词
    queries = logs.values_list('query', flat=True)
    word_count = Counter()
    for query in queries:
        words = jieba.cut(query)
        word_count.update(words)
    most_common_words = word_count.most_common(10)

    # 将日志和最常见的关键词传递到模板
    return render(request, 'search_logs.html', {
        'logs': logs,
        'most_common_words': most_common_words,
        'click_logs': click_logs  # 添加点击日志到上下文
    })

@csrf_exempt
def record_click(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        user = request.user
        # 检查用户是否已认证
        if user.is_authenticated:
            # 创建并保存新的点击日志条目
            ClickLog.objects.create(user=user, url=url)
            return JsonResponse({'status': 'success'})
        else:
            # 用户未登录的情况
            return JsonResponse({'status': 'unauthenticated'}, status=401)

    return JsonResponse({'status': 'error'}, status=400)