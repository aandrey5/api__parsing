import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/business/?stype=0']

    def parse(self, response: HtmlResponse):

        labirint_links = response.xpath("//div[@class= 'product-cover']/a/@href").extract()
        for link in labirint_links:
            #link_corr = self.allowed_domains[0] + link
            yield response.follow(link, callback=self.labirint_parse)
        next_page = response.xpath("//a[@class = 'pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)


        print()
    def labirint_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('auth', "//div[@class = 'authors']/a/text()")
        loader.add_xpath('price_main', "//span[@class = 'buying-priceold-val-number']/text()")
        loader.add_xpath('price_discount', "//span[@class = 'buying-pricenew-val-number']/text()")
        loader.add_xpath('rate', "//div[@id = 'rate']/text()")

        yield loader.load_item()

        #name = response.xpath('//h1/text()').extract_first()
        #url = response.url
        #auth = response.xpath("//div[@class = 'authors']/a/text()").extract()
        #price_main = response.xpath("//span[@class = 'buying-priceold-val-number']/text()").extract_first()
        #price_discount = response.xpath("//span[@class = 'buying-pricenew-val-number']/text()").extract_first()
        #price_rate = response.xpath("//div[@id = 'rate']/text()").extract_first()

        # yield JobparserItem(name=name, url=url, auth=auth, price_main=price_main,
        #                     price_discount=price_discount, price_rate=price_rate)

