# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from crawl_ip.items import CrawlIpItem


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/ip']

    # def parse(self, response):
    #     pass
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    # cookie = '__mta=147808136.1593241623225.1593394380772.1593394383733.19; uuid_n_v=v1; uuid=CBF269D0B84411EAB787AF911C0DA1B7D5B414D00A844CA9AB826A8A67B567BE; mojo-uuid=c4b625192d7f237345942348556f42b4; _lxsdk_cuid=172f499da63be-01f86fc7a07716-4353760-232800-172f499da64c8; _lxsdk=CBF269D0B84411EAB787AF911C0DA1B7D5B414D00A844CA9AB826A8A67B567BE; _csrf=4df92795d4e9c1d079257b756b8c45fdcff565b4f7aadbfe8fc5b6166a448474; mojo-session-id={"id":"3639644a398aaccc48bde3b6d2b8ee65","time":1593929528391}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593241623,1593331006,1593929528; mojo-trace-id=3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593929603; __mta=147808136.1593241623225.1593394383733.1593929603708.20; _lxsdk_s=1731d9a7628-17e-863-977%7C%7C4'
    # header = {'User-Agent': user_agent, 'Cookie': cookie}

    def start_requests(self):
        for i in range(10):
            url = f'https://maoyan.com/films?showType=3&offset={i*30}'
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        items = []
        movies = Selector(response = response).xpath('//div[@class="movie-hover-info"]')
        for movie in movies:
            item = CrawlIpItem()
            title = movie.xpath('./div/span/text()').get().strip()
            info = movie.xpath('./div/text()')
            movie_type = info[4].get().strip()
            date = info[-1].get().strip()
            item['title'] = title
            item['movie_type'] = movie_type
            item['date'] = date
            items.append(item)
        return items



