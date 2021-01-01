# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

from collections import defaultdict

def params_key(param_key):
    param_key = param_key.replace('\n','').replace('  ', '')
    return param_key

def params_item(param_item):
    param_item = param_item.replace('\n','').replace('  ', '')
    return param_item

def price_correct(price):
    if price:
        try:
            price = float(price.replace(' ',''))
            return price
        except Exception as e:
            print(e)


class JobparserLeroyItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field()
    param_key = scrapy.Field(input_processor=MapCompose(params_key))
    param_item = scrapy.Field(input_processor=MapCompose(params_item))
    info = scrapy.Field()
    #parameters = defaultdict(scrapy.Field(input_processor=MapCompose(params_clean), output_processor=TakeFirst()))
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_correct), output_processor=TakeFirst())
    _id = scrapy.Field()

