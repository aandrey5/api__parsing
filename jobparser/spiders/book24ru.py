import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=business']

    def parse(self, response: HtmlResponse):
        book_links = response.xpath("//a[@class = 'book-preview__title-link']/@href").extract()
        for link in book_links:
            yield response.follow(link, callback=self.book24_parse)
        next_page = response.xpath("//div[@class ='catalog-pagination__list']/a[contains(text(),'Далее')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)
        print()



    def book24_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('auth', "//span[@class = 'item-tab__chars-value']/a[@itemprop='author']/text()")
        loader.add_xpath('price_main', "//div[@class = 'item-actions__price-old']/text()")
        loader.add_xpath('price_discount', "//b[@itemprop = 'price']/text()")
        loader.add_xpath('rate', "//span[@class = 'rating__rate-value']/text()")

        yield loader.load_item()

        print()




        #book24_name = response.xpath("//h1/text()").extract_first()
        # book24_url = response.url
        # book24_auth = response.xpath("//span[@class = 'item-tab__chars-value']/a[@itemprop='author']/text()").extract()
        # book24_price_main = response.xpath("//div[@class = 'item-actions__price-old']/text()").extract_first()
        # book24_price_discount = response.xpath("//b[@itemprop = 'price']/text()").extract_first()
        # book24_rate = response.xpath("//span[@class = 'rating__rate-value']/text()").extract_first()

        # yield JobparserItem(name=book24_name, url=book24_url, auth=book24_auth, price_main=book24_price_main,
                            #price_discount=book24_price_discount, price_rate=book24_rate)


