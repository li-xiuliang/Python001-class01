if __name__ == '__main__':
    from spider.spiders.phone import PhoneSpider
    from spider.run_spider import Scraper

    scraper = Scraper()
    scraper.run_spiders()


# if __name__ == '__main__':
#     from scrapy.crawler import CrawlerProcess
#     from scrapy.utils.project import get_project_settings
#     settings = get_project_settings()
#     settings = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
#     process = CrawlerProcess(settings)
#     process.crawl(PhoneSpider)
#     process.join()