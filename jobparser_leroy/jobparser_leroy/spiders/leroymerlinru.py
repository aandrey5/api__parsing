import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from jobparser_leroy.jobparser_leroy.items import JobparserLeroyItem


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']


    def __init__(self, search):
        super(LeroymerlinruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']


    def parse(self, response: HtmlResponse):
        leroy_links = response.xpath("//a[@class = 'plp-item__info__title']")
        for link in leroy_links:
            yield response.follow(link, callback=self.parse_leroy)



    def parse_leroy(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserLeroyItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photo', "//source[contains(@media, 'min-width: 1024px')]/@srcset")
        loader.add_xpath('param_key', "//div[@class = 'def-list__group']/dt/text()")
        loader.add_xpath('param_item', "//div[@class = 'def-list__group']/dd/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[@slot = 'price']/text()")
        #loader.add_value('parameters', '')

        yield loader.load_item()




        print()

