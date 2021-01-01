# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pprint import pprint
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]

        return item
        print()

    def file_path(self, request, response=None, info=None, *, item=None):
        photo_id = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item["name"]}/{photo_id}.jpg'
        print()


class JobparserLeroyPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy

    def process_item(self, item, spider):
        length = len(item['param_item'])
        item['info'] = self.key_plus_para(item['param_key'], item['param_item'], length)
        del item['param_key']
        del item['param_item']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def key_plus_para(self, key, para, length):
        parameters = {}
        for i in range(length):
            parameters.update({key[i]: para[i]})
        return parameters
