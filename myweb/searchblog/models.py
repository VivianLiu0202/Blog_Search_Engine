from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from elasticsearch_dsl import Text, Date, Keyword, Integer, Document, Completion,Double
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer
# Elasticsearch连接配置
ES_HOST = "http://127.0.0.1:9200"
connections.create_connection(hosts=[ES_HOST])

my_analyzer = analyzer('ik_smart')

# Create your models here.

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

class CustomUser(AbstractUser):
    # add additional fields in here
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    favorite_field = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
    

#查询日志的model
class SearchQueryLog(models.Model):
    # 注意这里的变更，我们将get_user_model()的调用移动到方法内部
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} searched for {self.query} on {self.timestamp}"

# 查询点击日志
class ClickLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} clicked on {self.url} at {self.timestamp}"


#网页快照的model
class WebpageSnapshot(models.Model):
    url = models.URLField(unique=True)
    snapshot = models.TextField()  # 存储HTML内容
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Snapshot of {self.url} from {self.timestamp}"
    