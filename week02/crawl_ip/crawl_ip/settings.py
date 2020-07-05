# -*- coding: utf-8 -*-

# Scrapy settings for crawl_ip project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawl_ip'

SPIDER_MODULES = ['crawl_ip.spiders']
NEWSPIDER_MODULE = 'crawl_ip.spiders'

MYSQL_HOST      = 'localhost'
MYSQL_PORT      = 3306
MYSQL_USER      = 'root'
MYSQL_PASSWORD  = '123456'
MYSQL_CHARSET   = 'utf8mb4'
MYSQL_DATABASE  = 'test'
MYSQL_TABLE     = 'movie'




# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl_ip (+http://www.yourdomain.com)'
USER_AGENT = 'crawl_ip (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawl_ip.middlewares.CrawlIpSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawl_ip.middlewares.CrawlIpDownloaderMiddleware': 543,
#}

DOWNLOADER_MIDDLEWARES = {
   'crawl_ip.middlewares.CrawlIpDownloaderMiddleware': 543,
   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
   'crawl_ip.middlewares.RandomHttpProxyMiddleware':400,
}

HTTP_PROXY_LIST = [
    'http://45.70.200.183:999',
    'http://20.43.156.109:80',
    'http://186.233.104.25:8080'
]

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'crawl_ip.pipelines.CrawlIpPipeline': 300,
#}

ITEM_PIPELINES = {
   'crawl_ip.pipelines.process_mysql': 300,
}

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
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
