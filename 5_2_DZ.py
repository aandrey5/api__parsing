from selenium import webdriver
import ast
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from pprint import pprint

# БЛОК MongoDB
client = MongoClient('127.0.0.1', 27017)
db6 = client['mvideo']
mvideo_parse = db6.mvideo
mvideo_parse.delete_many({})

# Функц записи в базу товара
def record_mvideo(productId, name, price):
    mvideo_parse.insert_one({'productId': productId, 'name': name, 'price': price})

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://www.mvideo.ru/')
i = 1

list_id = []

while True:
    goods = driver.find_elements_by_xpath(
        "//ul[contains(@data-init-param, 'Хиты продаж')]/li//a[@class = 'sel-product-tile-title']")
    time.sleep(0.5)
    for el in goods:
        good = (el.get_attribute('data-product-info').replace("""\n'
     '\t\t\t\t\t""", ''))
        # Функция принудительно превращает строку, похожую на словарь в словарь
        good = ast.literal_eval(good)
        # отладка -проверка извлечения данных из словаря
        #print(good['productId'], good['productName'], good['productPriceLocal'])
        productId = good['productId']

        # если id нет в списке - то добавляем этот элемент и пишем строку в базу
        # если есть - пропускаем, наматываем счетчик пропусков чтобы потом выйти из главного цикла
        if productId not in list_id:
            list_id.append(good['productId'])
            record_mvideo(good['productId'], good['productName'], good['productPriceLocal'])
            #print(list_id)
        else:
            i += 1
            pass
    # отладка  - раздел нового внутреннего цикла
    #print('раздел')
    time.sleep(1)
    button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'next-btn.c-btn.c-btn_scroll-horizontal.c-btn_icon.i-icon-fl-arrow-right')))
    time.sleep(1)
    button.click()
    time.sleep(2)

    # счетчик повторений записей дублирующихся товаров, поставлен как TimeOut ожидания
    if i > 40:
        break
# отладка
#print(list_id)
print('Готово')
# ПРОВЕРИМ БАЗУ

for el in mvideo_parse.find({}):
    pprint(el)





