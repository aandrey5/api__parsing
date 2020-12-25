import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


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
        book_name = response.xpath("//h1/text()").extract_first()
        book_url = response.url
        book_auth = response.xpath("//span[@class = 'item-tab__chars-value']/a[@itemprop='author']/text()").extract()
        book_price_main = response.xpath("//div[@class = 'item-actions__price-old']/text()").extract_first()
        book_price_discount = response.xpath("//b[@itemprop = 'price']/text()").extract_first()
        book_rate = response.xpath("//span[@class = 'rating__rate-value']/text()").extract_first()

        yield JobparserItem(book_name=book_name, book_url=book_url, book_auth=book_auth, book_price_main=book_price_main,
                            book_price_discount=book_price_discount, book_rate=book_rate)
        print()

