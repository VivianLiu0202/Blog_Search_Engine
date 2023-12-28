import scrapy
from blog_spider.items import BlogSpiderItem
from blog_spider.settings import COOKIE,USER_AGENT
from blog_spider.utils.common import get_md5
import random
from typing import Iterable
import scrapy
from scrapy.http import Request
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars
from fake_useragent import UserAgent

class BlogSpider(scrapy.Spider):
    name = "blog"
    allowed_domains = ["blog.51cto.com"]
    start_urls = ["https://blog.51cto.com"]
    ua = UserAgent()
    headers = {
        "HOST": "blog.51cto.com",
        "Referer": "https://blog.51cto.com/",
        "User-Agent": ua.chrome,
        "cookie": COOKIE
    }

    def parse(self, response):
        with open('/Users/liuvivian/Blog_Search_Engine/blog_spider/blog_spider/spiders/blogtype.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        #分批读取data，先读取10个
        for i in data[0:68]:
            print(i);
            if i['TypeUrl'] is not None:
                for url in i['TypeUrl']:
                    self.logger.debug("start to parse url: %s" % url)
                    yield scrapy.Request(url=url, callback=self.parse_article_list, headers=self.headers)
        #yield scrapy.Request(url="https://blog.51cto.com/nav/openstack_p_1", callback=self.parse_article_list, headers=self.headers)
        

    """
    解析文章列表页面
    """
    def parse_article_list(self, response):
        articles = response.css('div.article-item')
        for article in articles:
            article_url = article.css('a::attr(href)').get()

            # 提取文章摘要内容
            article_abstract = remove_tags(article.css('div.content').get()).strip()
            article_abstract = replace_escape_chars(article_abstract)
            # article_abstract = re.sub(r'[^\w\s]',' ',article_abstract,flags=re.UNICODE)
            # article_abstract = re.sub(r'_', '', article_abstract)  # 移除下划线
            # article_abstract = re.sub(r'#', '', article_abstract)  # 移除下划线 
            # article_abstract = re.sub(r'\s+', ' ', article_abstract).strip() 

            yield response.follow(
                url = article_url,
                callback = self.parse_article_content,
                headers = self.headers,
                meta = {'article_abstract': article_abstract}
            )


    """
    解析文章内容页面
    """
    def parse_article_content(self, response):
        item = BlogSpiderItem()
        
        # 使用remove_tags处理器去除HTML标签
        item['abstract'] = response.meta['article_abstract']
        item['url'] = response.url
        item['title'] = response.css('h1::text').get()
        item['author'] = response.xpath('//p[@class="clearfix mess-line1"]/a/text()').extract_first()

        # content_parts = response.xpath('//div[@class="con artical-content editor-preview-side"]').getall()
        # if not content_parts:
        #     content_parts = response.xpath('//div[@class="editor-container container am-engine"]').getall()

        content_parts = response.xpath('//div[@class="article-content-wrap"]').getall()
        content = ''.join(content_parts).strip()
        content = replace_escape_chars(content)
        # 清除多余的空白字符
        content = remove_tags(content).strip()
        #content = re.sub(r'[\n\s\|]+', ' ', content)
        # 将清洗后的文本添加到item
        item['content'] = content

        # 使用CSS选择器提取时间字符串
        time_str = response.xpath('//p[@class="clearfix mess-line1"]/time/text()').extract_first()
        # 将字符串转换为datetime对象
        if time_str:
            pub_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            # 格式化时间为ISO 8601格式
            formatted_time = pub_time.isoformat()
            # 将格式化后的时间添加到item
        item['pubTime'] = formatted_time

        item['relate'] = response.css('div.about-aticle-list a::attr(href)').getall()
        item['urlID'] = get_md5(response.url)
        item['PR'] = 0 #初始化PR

        yield item