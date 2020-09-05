from analyze.celery import app
from . import run_spider
from phone.spider.spider.spiders.phone import PhoneSpider
import os
from .sentiment import data_clean

@app.task()
def task1():
    print('scrapy start')
    os.system("cd ./phone/spider && scrapy crawl phone")
    print('scrapy finish')
    pd_data = data_clean()
    pd_data.update_date()
    print('finish')


# @app.task()
# def task1():
#      print('test1')
#      scraper = run_spider.Scraper()
#      scraper.run_spiders()
#      #run_spider.spider_phone(PhoneSpider)
#      print('test2')

# @app.task()
# def task2():
#      return 'test2'