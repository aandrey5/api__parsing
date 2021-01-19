# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    type_data = scrapy.Field()
    username = scrapy.Field()
    user_id = scrapy.Field()
    id_podpischik = scrapy.Field()
    photo = scrapy.Field()
    podpischik_name = scrapy.Field()
    podpis_data = scrapy.Field()
    id_podpiska = scrapy.Field()
    podpiska_name = scrapy.Field()
    podpiska_data = scrapy.Field()
    _id = scrapy.Field()




