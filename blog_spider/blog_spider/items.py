# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from blog_spider.models.es_blog import BlogType

class BlogTypeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    TypeWords = scrapy.Field()
    TypeUrl = scrapy.Field()

#根据字符串生成搜索建议数组
def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    used_words = set() #去重
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = index.analyze(text)
            anylyzed_words = set([r['token'] for r in words['tokens'] if len(r['token'])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()
        
        if new_words:
            suggests.append({'input':list(new_words), 'weight':weight})
    return suggests

class BlogSpiderItem(scrapy.Item):
    title = scrapy.Field() # 标题
    author = scrapy.Field() # 作者
    abstract = scrapy.Field() # 摘要
    url = scrapy.Field() # 文章链接
    urlID = scrapy.Field() # 文章链接ID
    pubTime = scrapy.Field() # 发布时间
    content = scrapy.Field() # 文章内容
    relate = scrapy.Field() # 相关文章
    PR = scrapy.Field() # PR值

    def save_to_es(self):
        blog = BlogType()
        blog.title = self['title']
        blog.abstract = self['abstract']
        blog.url = self['url']
        blog.pubTime = self['pubTime']
        blog.content = self['content']
        blog.relate = self['relate']
        blog.suggest = gen_suggests(BlogType._doc_type.index, ((blog.title, 7), (blog.abstract, 3)))

        blog.save()
        return


