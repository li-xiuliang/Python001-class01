# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from spider.items import SpiderItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    cookie = 'll="118297"; bid=XmT_jKebEMc; __yadk_uid=e7uWxdfinEsO5ROs9IFBKG9G3MT42R4A; _vwo_uuid_v2=DFA34F66CEE26A258CD89DE50185433F5|5c55fbd028ce2f94d4c363bba14561a9; __gads=ID=39631da6401e6e22:T=1593091817:S=ALNI_Mbb2C2AoW76bgZ-feATgn1LsCJAKw; __utmz=223695111.1594186364.3.2.utmcsr=dogedoge.com|utmccn=(referral)|utmcmd=referral|utmcct=/; douban-fav-remind=1; __utmc=30149280; __utmz=30149280.1596167485.5.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=30149280.1104063331.1593090649.1596167485.1596182787.6; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1596183250%2C%22https%3A%2F%2Fwww.dogedoge.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1343079845.1593090649.1594186364.1596183250.4; __utmb=223695111.0.10.1596183250; __utmc=223695111; ap_v=0,6.0; __utmb=30149280.2.10.1596182787; _pk_id.100001.4cf6=6b694663bf0f9c84.1593090649.4.1596185724.1594186363.'
    
    header = {'User-Agent': user_agent, 'Cookie': cookie}
    
    # def parse(self, response):
    #     pass

    def start_requests(self):
        url = 'https://movie.douban.com/subject/26871906/comments?status=P'
        yield scrapy.Request(url = url, callback=self.parse)
    
    def parse(self, response):
        items = []
        shorts = Selector(response=response).xpath("//span[@class='short']")
        stars = Selector(response=response).xpath("//span[starts-with(@class, 'allstar')]")
        votes = Selector(response=response).xpath("//span[@class='votes']")
        for i in range(len(shorts)):
            item = SpiderItem()
            item['short'] = shorts[i].xpath('./text()').extract()[0]
            item['star'] = stars[i].xpath('./@class').extract()[0][7:9]
            item['recommend'] = stars[i].xpath('./@title').extract()[0]
            item['vote'] = votes[i].xpath('./text()').extract()[0]
            items.append(item)
        print(items)
        return items



