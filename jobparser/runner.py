from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser.spiders.labirintru import LabirintruSpider
from jobparser.spiders.book24ru import Book24ruSpider
from jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(Book24ruSpider)
    process.crawl(LabirintruSpider)


    process.start()




