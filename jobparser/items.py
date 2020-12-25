# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    labirint_name = scrapy.Field()
    labirint_url = scrapy.Field()
    labirint_auth = scrapy.Field()
    labirint_price_main = scrapy.Field()
    labirint_price_discount = scrapy.Field()
    labirint_price_rate = scrapy.Field()
    book_name = scrapy.Field()
    book_url =  scrapy.Field()
    book_auth = scrapy.Field()
    book_price_main = scrapy.Field()
    book_price_discount = scrapy.Field()
    book_rate = scrapy.Field()
    _id = scrapy.Field()
