import scrapy
from blog_spider.items import BlogSpiderItem,BlogTypeItem
from blog_spider.settings import COOKIE,USER_AGENT
import random
from typing import Iterable
import scrapy
from scrapy.http import Request
import json
import re
from bs4 import BeautifulSoup
import datetime

class BlogtypeSpider(scrapy.Spider):
    name = "blogType"
    allowed_domains = ["blog.51cto.com"]
    start_urls = ["https://blog.51cto.com/nav"]
    headers = {
        "HOST": "blog.51cto.com",
        "Referer": "https://blog.51cto.com/",
        "User-Agent": random.choice(USER_AGENT),
        "cookie": COOKIE
    }

    def parse(self,response):
        # 解析类别页面并遍历子类别
        category_list = response.css('div.nav-box')
        for category in category_list.css('a'):
            # type_item['TypeWords'] = category.css('::text').get()  # 提取链接文本
            # type_item['TypeUrl'] = category.css('::attr(href)').get()  # 提取链接URL
            url = category.css('::attr(href)').get()  # 提取链接URL
            yield response.follow(url=url, callback=self.parse_category)
    
    def parse_category(self,response):
        # 解析子类别页面并遍历分页
        minicategory_list = response.css('div.reclassify')
        for minicategory in minicategory_list.css('a'):
            type_name = minicategory.css('::text').get()
            miniurl = minicategory.css('::attr(href)').get()
            yield response.follow(url=miniurl, callback=self.parse_typepage, meta={'type_name': type_name,'urls': []})


    def parse_typepage(self,response):
        # 解析文章列表页面并遍历文章详情
        type_name = response.meta['type_name']
        url = response.meta['urls']

        for page in range(1,20):
            page_url = f"{response.url}_p_{page}"
            url.append(page_url)
        
        type_item = BlogTypeItem()
        type_item['TypeWords'] = type_name
        type_item['TypeUrl'] = url
        yield type_item
        



