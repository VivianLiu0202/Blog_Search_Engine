BOT_NAME = "blog_spider"

SPIDER_MODULES = ["blog_spider.spiders"]
NEWSPIDER_MODULE = "blog_spider.spiders"


USER_AGENT = [ "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "blog_spider.middlewares.BlogSpiderSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "blog_spider.middlewares.BlogSpiderDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "blog_spider.pipelines.BlogSpiderPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

FEED_FORMAT = 'json'
FEED_URI = 'output1.json'

ES_HOST = "127.0.0.1:9200"
COOKIE = "www51cto=7FFD9C5F21207591ED844FC878528956gWQu; Hm_lvt_110fc9b2e1cae4d110b7959ee4f27e3b=1678903001; callback_api_url=https%3A%2F%2Fhome.51cto.com%2Findex%3Ffrom_service%3Dblog%26scene%3Dlogin1%26reback%3Dhttps%3A%2F%2Fblog.51cto.com%2F; pub_cookietime=2592000; pub_auth_profile=Ujex%2Fmg9Dr6iWDfQT6EvfefiQ3go72uTn94je9FIdbg%3D; pub_sauth1=FhwPUV1XVFtVUQUABgoHPQUFAFBeBwEBa1IAVAZUVQRTVAE; pub_sauth2=aa009d30ff7022ef991af723e1618972; pub_wechatopen=DgZDExYRDi1xcW1YF3AvXl9EcgE2VnB2LVsaUDwLN3InJgwVPA91NGQDRnsqTz9VAVFXOxdCeV9SakAcAQZXUFFdXwBcBgAEUgQDBGoIUQQHAwNUVAIN; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216448540%22%2C%22first_id%22%3A%22186e5b3b72d2a6-0d3e06f44de548-1e525634-1484784-186e5b3b72e1d1a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22186e5b3b72d2a6-0d3e06f44de548-1e525634-1484784-186e5b3b72e1d1a%22%7D; aliyungf_tc=cbe1037263f9a91d4dd22edb204cd6e8186bdc9e8797e823eb1b384cf168f68e; acw_tc=ac11000117033418473154481eec8d1d7c385a1af7e28c7b2a614230907839; acw_sc__v3=6586ef20f2e3520bf674e9eb3ca237b0c718b24c; PHPSESSID=s20ls0s72vliv16l8l2t5bphbr; _identity=4b7bfeb7ea0c84a8c8e0d016cef3b11d6cbedb05e07adbb75904bf23f6afab37a%3A2%3A%7Bi%3A0%3Bs%3A9%3A%22_identity%22%3Bi%3A1%3Bs%3A21%3A%22%5B16448540%2Ctrue%2C86400%5D%22%3B%7D; cssLoaded=%2Fpcnewindex; Hm_lvt_2283d46608159c3b39fc9f1178809c21=1703001896,1703341860; Hm_lpvt_2283d46608159c3b39fc9f1178809c21=1703341870; ssxmod_itna2=Qu0=iK0IjKD5i=DXDnD+r8dD7YHH4iththb5hWD6E81ex05503it5uFWttk50FIhLDihuCDkTUOhb8m7iC=a+qO0LkCKmYaIt5FevPd8vpBLHpxvUeEbpFHRtAMO01fm68YWGxAPCWSQV43NvYlAV3QreXM6eseoerjEKhnUOYRR3HjUM9lXDuQnOin+jDjn6/w+b50dV8cXHplcWpW9FLe4H5=cW5MNksP4FM=Bsq8iCDKaIETraZ12Tw9ipijUGGiq7GYhCKAaHe5A=3Anq9KK3BPiqw0azr3x5Cajjii/ePHa0Eyzu8zRGOq7Gcua7xK3iaew1xW1gYdWDCe3elu1S0dqBOaOhUqC=Eas3ealDWB+iBDPANN8DFkKXCbLSrC4Tz3=7bTWMQWuxCxTFBpNR4vgrvjYf2Ax1EfxAt=EgAEw+AT6oWL751EoAshD4qav3SrWBxhR573em2NYWoma7lf6kiPD7Q1i9ilRxn9d/D2ihMIyGGR7zwrEHhGqYWD0xxYnx7QGAmBPNw/CfwAhC7xzhG+4eSmOFz2TIDDjKDekq4D=; ssxmod_itna=eqfx0DRDnD9Ao7KGHfhCDU2Dh3nUDxYvLdD/3mDnqD=GFDK40ooHPDCQm/itU2Q17bhxYQoSIrP+774qe4IGCdAtebDneG0DQKGmDBKDSDWKD9mCT4GGmxBYDQxAYDGDDpcDGdXORD7hU9+LtjYTQ6QwtDm+Q0DGQRDitoxivDyLNS08DSDDfYxB=DxA30D7UlYwdDbqDuFpQ5EqDLmnnaxPQDb2eyDPWDtdu0B4DHUTN/YTHoG0DEn23c+8DYKBKrzD45mDqQY0xqWiholDwxWDqr0Bvb+F4qeD"