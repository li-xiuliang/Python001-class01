# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

MYSQL_HOST      = 'localhost'
MYSQL_PORT      = 3306
MYSQL_USER      = 'root'
MYSQL_PASSWORD  = '123456'
MYSQL_CHARSET   = 'utf8mb4'
MYSQL_DATABASE  = 'douban'
MYSQL_TABLE     = 'comments_dbcomment'

# class SpiderPipeline:
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
            host = MYSQL_HOST,
            port = MYSQL_PORT,
            user = MYSQL_USER,
            password = MYSQL_PASSWORD,
            charset = MYSQL_CHARSET,
            database = MYSQL_DATABASE,
            table = MYSQL_TABLE
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(host = self.host, 
                                  port = self.port,
                                  user = self.user,
                                  password = self.password,
                                  database = self.database,
                                  charset = self.charset             
        )
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