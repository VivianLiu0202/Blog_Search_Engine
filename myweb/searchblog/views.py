from django.shortcuts import render
from .models import BlogIndex
from elasticsearch_dsl import Search
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

    return render(request, 'search.html', {'query_type': query_type, 'query': query, 'results': results})