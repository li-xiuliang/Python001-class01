import os
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from phone.spider.spider.spiders.phone import PhoneSpider

from crochet import setup
import sys

sys.path.append('.')

class Scraper():
    def __init__(self):
        settings_file_path = 'phone.spider.spider.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE',settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spiders = PhoneSpider

    def run_spiders(self):
        self.process.crawl(self.spiders)
        self.process.start()

    # def spider_phone(self):
    #     #setup()
    #     settings = get_project_settings()
    #     runner = CrawlerRunner(settings = {
    #         'MYSQL_CONNECTION': 'mysql+mysqlconnector://root:123456@localhost/phonedb?charset=utf8mb4',
    #         'DEFAULT_REQUEST_HEADERS': {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #         'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,zh-CN;q=0.6',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    #         'Host': 'www.smzdm.com'
    #         },
    #         'ITEM_PIPELINES': {
    #         'spider.pipelines.SpiderPipeline': 300,
    #         },
    #     })
    #     runner.crawl(PhoneSpider, 'all')
    #     runner.join()

# class Scraper():
#     def spider_phone(self):
#         process = CrawlerProcess(get_project_settings())
#         process.crawl(PhoneSpider)
#         process.start()
#         process.join()