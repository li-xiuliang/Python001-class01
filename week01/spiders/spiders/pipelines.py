# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import os.path

class SpidersPipeline:
    def process_item(self, item, spider):
        i = [{'title': item['title'], 'movie_type': item['movie_type'], 'date': item['date']}]
        #i = [(item['title'], item['movie_type'], item['date'])]
        i_p = pd.DataFrame(i)
        if os.path.isfile('./maoyan.csv'):
            i_p.to_csv('./maoyan.csv', encoding = 'utf-8', mode = 'a', columns = ['title', 'movie_type', 'date'], index = False, header = False)
        else:
            i_p.to_csv('./maoyan.csv', encoding = 'utf-8', mode = 'w', columns = ['title', 'movie_type', 'date'], index = False, header = True)
