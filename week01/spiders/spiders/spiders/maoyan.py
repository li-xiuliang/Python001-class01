# -*- coding: utf-8 -*-
import scrapy
from spiders.items import SpidersItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    cookie = '__mta=147808136.1593241623225.1593331088357.1593332474371.15; uuid_n_v=v1; uuid=CBF269D0B84411EAB787AF911C0DA1B7D5B414D00A844CA9AB826A8A67B567BE; mojo-uuid=c4b625192d7f237345942348556f42b4; _lxsdk_cuid=172f499da63be-01f86fc7a07716-4353760-232800-172f499da64c8; _lxsdk=CBF269D0B84411EAB787AF911C0DA1B7D5B414D00A844CA9AB826A8A67B567BE; _csrf=20c9cf413ecb7c4c9b92dc96d8a35ff39ee3ef626a4f634a38d574a46d974b2f; mojo-session-id={"id":"1308c6265db8fbcb9de25e47406e5f9d","time":1593331005481}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593241623,1593331006; __mta=147808136.1593241623225.1593270207807.1593331005944.13; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593332474; mojo-trace-id=5; _lxsdk_s=172f9edb8df-bc4-ced-d2d%7C%7C7'
    header = {'User-Agent': user_agent, 'Cookie': cookie}

    def start_requests(self):
        for i in range(10):
            url = f'https://maoyan.com/films?showType=3&offset={i * 30}'
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        items = []
        movies = Selector(response = response).xpath('//div[@class="movie-hover-info"]') 
        for movie in movies:
            item = SpidersItem()
            title = movie.xpath('./div/span/text()').get().strip()
            info = movie.xpath('./div/text()')
            movie_type = info[4].get().strip()
            date = info[-1].get().strip()
            item['title'] = title
            item['movie_type'] = movie_type
            item['date'] = date
            items.append(item)
        return items

    



        
        
        
