# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pprint import pprint


class InstaparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram

    def process_item(self, item, spider):

        collection = self.mongo_base[spider.name]
        # pass
        collection.insert_one(item)
        # print()
        return item


# -----ЗАПУСТИТЬ ТОЛЬКО pipelines -----------

# Универсальный метод вывода данных по пользователю либо типу подписка / подписчиков (можно было конечно в базе одно поле сделать)

def query(query_user, query_type):
    # условие меняет наполнение в выводе pprint
    if query_type == 'podpiska':
        variant = 'podpiska_name'
    else:
        variant = 'podpischik_name'

    client = MongoClient('localhost', 27017)
    db = client.instagram
    collection = db.instagram

    for el in collection.find({'type_data': query_type, 'username': query_user}):
        pprint('Пользователь: '+ ' ' + el['username'] + ' / ' + query_type + ' / ' + el[variant])

# смотрим подписки выбранного пользователя
query('kolia.baran','podpiska')

# смотрим подписчиков другого выбранного пользователя

query('babai.vasia','podpischik')