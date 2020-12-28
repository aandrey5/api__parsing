# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import MapCompose, TakeFirst


def process_price_main(price_main):
    try:
        price_main = int(price_main.replace(' р.', '').replace(' ', ''))
        return price_main
    except:
        return price_main


def process_price_discount(price_discount):
    try:
        price_discount = int(price_discount.replace(' р.', '').replace(' ', ''))
        return price_discount
    except:
        return price_discount


class JobparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    auth = scrapy.Field(output_processor=TakeFirst())
    price_main = scrapy.Field(input_processor=MapCompose(process_price_main), output_processor=TakeFirst())
    price_discount = scrapy.Field(input_processor=MapCompose(process_price_discount), output_processor=TakeFirst())
    rate = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
    print()
