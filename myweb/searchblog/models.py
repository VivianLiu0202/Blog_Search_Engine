from django.db import models
from django.conf import settings
from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion,Double
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer
# Elasticsearch连接配置
ES_HOST = "http://127.0.0.1:9200"
connections.create_connection(hosts=[ES_HOST])

my_analyzer = analyzer('ik_smart')

# Create your models here.
from django.contrib.auth.models import AbstractUser

class BlogIndex(Document):
    title = Text(analyzer="ik_max_word")
    author = Text(analyzer="ik_smart")
    abstract = Text(analyzer="ik_max_word")
    url = Keyword()
    pubTime = Date()
    content = Text(analyzer="ik_max_word")
    relate = Keyword()
    PR = Double()

    class Index:
        name = 'blog'