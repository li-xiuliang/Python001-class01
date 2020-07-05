# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

# class CrawlIpPipeline:
#     def process_item(self, item, spider):
#         return item

class process_mysql():
    def __init__(self, host, port, user, password, charset, database, table):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.database = database
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            port = crawler.settings.get('MYSQL_PORT'),
            user = crawler.settings.get('MYSQL_USER'),
            password = crawler.settings.get('MYSQL_PASSWORD'),
            charset = crawler.settings.get('MYSQL_CHARSET'),
            database = crawler.settings.get('MYSQL_DATABASE'),
            table = crawler.settings.get('MYSQL_TABLE')
        )
    
    def open_spider(self, spider):
        self.db = pymysql.connect(host = self.host, port = self.port, user = self.user, password = self.password, database = self.database, charset = self.charset)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
    
    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (self.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
        



