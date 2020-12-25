# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books_all_sites

    def process_item(self, item, spider):
        # if spider.name = 'labirintru':
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        print()
        return item
