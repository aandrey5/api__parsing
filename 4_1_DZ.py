import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

# БЛОК MongoDB
client = MongoClient('127.0.0.1', 27017)
db4 = client['news']
news_db = db4.news

# DROP TABLE IF EXISTS )
news_db.delete_many({})

# Функц записи в базу новости
def record_news(source, name, link, time):
    news_db.insert_one({'source': source, 'name': name, 'link': link,'time': time })


# БЛОК ЗАПРОСОВ И URL
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}

url_yandex = 'https://yandex.ru/news'
url_mail = 'https://news.mail.ru/'
url_lenta = 'https://lenta.ru/'

response_ya = requests.get(url_yandex, headers=header)
response_mail = requests.get(url_mail, headers=header)
response_lenta = requests.get(url_lenta, headers=header)


dom_ya = html.fromstring(response_ya.text)
dom_mail = html.fromstring(response_mail.text)
dom_lenta = html.fromstring(response_lenta.text)




news = []


# БЛОК ИСТОЧНИКОВ НОВОСТЕЙ
# YANDEX
items_ya = dom_ya.xpath('//div[@class = "mg-grid__col mg-grid__col_xs_4" ]')
for item in items_ya:
    news = {}
    source = item.xpath('.//span[@class = "mg-card-source__source" ]/a/text()')
    name = item.xpath('.//h2[@class = "mg-card__title" ]/text()')
    link = item.xpath('.//article/a/@href')
    time = item.xpath('.//span[@class = "mg-card-source__time" ]/text()')

    news['source'] = source
    news['name'] = name
    news['link'] = link
    news['time'] = time

    record_news(source, name, link, time)

    #pprint(news)
    #pprint(name + source + link + time)


# MAIL
i = 0
items_mail = dom_mail.xpath('//td/div/a')
list_source_mail = []
list_time_mail = []
for item in items_mail:
    news_m = {}
    name_mail = item.xpath('//td/div/a/span/span[contains(@class, "photo__title photo__title_new photo__title_new_hidden js-topnews__notification")]/text()')
    link_mail = item.xpath('//td/div/a/@href')

    resp_source_mail = requests.get(link_mail[i], headers=header )
    dom_resp = html.fromstring(resp_source_mail.text)
    source_mail = dom_resp.xpath("//a[@class = 'link color_gray breadcrumbs__link']/span[@class = 'link__text']")

    for el in source_mail:
        list_source_mail.append(el.xpath("//a[@class = 'link color_gray breadcrumbs__link']/span[@class = 'link__text']/text()")[0])
        list_time_mail.append(el.xpath("//span[@class = 'note__text breadcrumbs__text js-ago']/@datetime"))

    #pprint(list_time_mail[i][0] + ' '+ list_source_mail[i] +' ' + name_mail[i] + " " + link_mail[i])

    news_m['source'] = list_source_mail[i]
    news_m['name'] = name_mail[i]
    news_m['link'] = link_mail[i]
    news_m['time'] = list_time_mail[i][0]

    record_news(list_source_mail[i], name_mail[i], link_mail[i], list_time_mail[i][0])

    i += 1

    #pprint(news_m)



# LENTA

i = 0
items_lenta = dom_lenta.xpath("//div[@class = 'span4']/div[@class = 'item']")
for elem in items_lenta:
    news_lenta = {}
    source_lenta = url_lenta
    name_lenta = elem.xpath("./a/text()")
    link_lenta = elem.xpath("./a/@href")
    time_lenta = elem.xpath("//div[@class = 'span4']/div[@class = 'item']/a/time/@datetime")

    news_lenta['source'] = source_lenta
    news_lenta['name'] = name_lenta[0].replace('\xa0', ' ')
    news_lenta['link'] = url_lenta + link_lenta[0]
    news_lenta['time'] = time_lenta[i]

    record_news(source_lenta, name_lenta[0].replace('\xa0', ' '), url_lenta + link_lenta[0], time_lenta[i])

    i += 1

    #pprint(news_lenta)


# ПРОВЕРИМ БАЗУ

for el in db4.news.find({}):
    pprint(el)

