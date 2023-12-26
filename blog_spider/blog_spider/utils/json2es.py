from elasticsearch_dsl import connections, Document, Keyword, Text, Integer,Float, Date, Completion, analyzer,Double
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index
from datetime import datetime
import json

# Elasticsearch连接配置
ES_HOST = "127.0.0.1:9200"
connections.create_connection(hosts=[ES_HOST])

my_analyzer = analyzer('ik_smart')
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

# 文档类型定义
class BlogType(Document):
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


# 检查索引是否存在，如果存在则删除
index = Index('blog')
if index.exists():
    print("Deleting existing index...")
    index.delete()  # 删除已存在的索引

# 重新创建索引
print("Creating new index...")
BlogType.init()

# JSON数据文件路径
json_file_path = '/Users/liuvivian/Blog_Search_Engine/blog_spider/finaloutput.json'

# 读取JSON文件
with open(json_file_path, 'r') as file:
    data = json.load(file)

# 导入数据到Elasticsearch
def import_to_elasticsearch(data):
    # 检查是否已存在该文档（根据URL或其他唯一字段）
    search_result = BlogType.search().filter("term", url=data["url"]).execute()
    if search_result.hits.total.value > 0:
        print("Document already exists:", data["url"])
        return

    # 创建文档实例
    blog_doc = BlogType(
        title=data["title"],
        author=data["author"],
        abstract=data["abstract"],
        url=data["url"],
        pubTime=datetime.strptime(data["pubTime"], "%Y-%m-%dT%H:%M:%S"),
        content=data["content"],
        relate=data["relate"],
        PR=data["PR"]
    )

    # 保存文档
    blog_doc.save()
    print("Document added:", data["url"])

# 执行导入操作
for item in data:
    import_to_elasticsearch(item)