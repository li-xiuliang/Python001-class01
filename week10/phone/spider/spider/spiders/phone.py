# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from datetime import datetime
import re

from ..items import SpiderItem


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['www.smzdm.com']
    start_urls = ['https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/']

    def parse(self, response):
        sel = Selector(response)
        phone_urls = sel.xpath('//h5[@class="feed-block-title"]//a//@href')
        for url_xpath in phone_urls:
            url = ''.join(url_xpath.extract()).strip()
            phone_id = str(url.split('/')[-2])
            yield Request(url = url, dont_filter = True, meta = {'phone_id': phone_id}, callback = self.phone_page)

        next_page = sel.xpath('//li[(@class="page-turn  next-page")]//a//@href')
        if next_page:
            yield Request(''.join(next_page.extract()).strip(), dont_filter = True, callback = self.parse)

    def phone_page(self, response):
        sel = Selector(response)
        phone_info = {}
        phone_info['id'] = response.meta['phone_id']
        name = sel.xpath('//h1[@class="title J_title"]//text()')
        phone_info['name'] = ''.join(name.extract()).strip() if name else ''
        price = sel.xpath('//div[@class="price"]//text()').re_first('\d+')
        phone_info['price'] = int(price) if price else 0
        update_time = sel.xpath('//span[@class="time"]//text()')
        phone_info['sell_time'] = ''
        if update_time:
            phone_info['sell_time'] = ''.join(update_time.extract()).strip()
        author = sel.xpath('//div[@class = "author-info J_author_info"]//span[@class="name"]//text()')
        phone_info['author'] = ''.join(author.extract()).strip() if author else ''
        rating_worthy_num = sel.xpath('//span[@id = "rating_worthy_num"]//text()')
        phone_info['rating_worthy_num'] = int(''.join(rating_worthy_num.extract()).strip()) if rating_worthy_num else 0
        rating_unworthy_num = sel.xpath('//span[@id = "rating_unworthy_num"]//text()')
        phone_info['rating_unworthy_num'] = int(''.join(rating_unworthy_num.extract()).strip()) if rating_unworthy_num else 0

        descrip1 = sel.xpath('//article[@class = "txt-detail"]/div[@class="describe"]//text()')
        descrip2 = sel.xpath('//article[@class = "txt-detail"]/p/text()')
        descrip3 = sel.xpath('//div[@class="baoliao-block"]//p//text()')
        phone_info['description'] = ''
        if descrip1:
            phone_info['description'] += ''.join(descrip1.extract()).strip()
        if descrip2:
            phone_info['description'] += ''.join(descrip2.extract()).strip()
        if descrip3:
            phone_info['description'] += ''.join(descrip3.extract()).strip()
        yield Request(response.url, meta = {'phone_info': phone_info}, callback = self.comments_page, dont_filter = True)

    def comments_page(self, response):
        sel = Selector(response)
        comments = sel.xpath('//div[@class="tab_info"][1]//li[@class="comment_list"]')
        phone_info = response.meta['phone_info']
        comments_info = {}
        for comment_xpath in comments:
            comments_info['phone_id'] = phone_info['id']
            comments_id = comment_xpath.xpath('./div[@class="comment_conBox"]/div[@class="comment_avatar_time "]/a[@class="a_underline user_name"]//@href')
            comments_info['comments_id'] = ''.join(comments_id.extract()).split('/')[-2].strip() if comments_id else ''
            comments_name = comment_xpath.xpath('./div[@class="comment_conBox"]/div[@class="comment_avatar_time "]/a[@class="a_underline user_name"]/span/text()')
            comments_info['name'] = ''.join(comments_name.extract()).strip() if comments_name else ''
            cell = comment_xpath.xpath('./div[@class="comment_avatar"]/span/text()')
            comments_info['cell'] = ''.join(cell.extract()).strip() if cell else ''
            content = comment_xpath.xpath('./div[@class="comment_conBox"]//div[@class="comment_con"]//span[@itemprop="description"]//text()')
            comments_info['content'] = ''.join(content.extract()).strip() if content else ''
            item = SpiderItem()
            item['phone_info'] = phone_info
            item['comments_info'] = comments_info
            yield item
        next_page = sel.xpath('//div[@class="tab_info"]//li[@class="pagedown"]/a/@href')
        if next_page:
            url = ''.join(next_page.extract()).strip()
            yield Request(url = url, meta = {'phone_info': phone_info}, callback = self.comments_page, dont_filter = True)

        

