from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
from pprint import pprint

# MongoDB блок
client = MongoClient('127.0.0.1', 27017)
db3 = client['vacancy_123']
vacancies = db3.vacancies
#vacancies.delete_many({})


# ИНТЕРАКТИВ
variant_record = int(input("Выберите вариант записи вакансий:\n1 - полностью записать в базу\n2 - только новые\nВведите номер: "))
if variant_record == 2:
    print('Если при 2м варианте не печатаются вакансии, то новых нет')
print('------- работаем ---------')

# очищаем таблицу в случае выбора первого варианта по полной записи в базу
if variant_record == 1:
    vacancies.delete_many({})


# ЗАДАНИЕ 1 Функция записыват данные в базу
def record_vacancy(href_vac, vac_name, min, max, val):
    vacancies.insert_one({'_1_vacancy': vac_name, '_2_sal_min': int(min), '_3_sal_max': int(max), '_4_href': href_vac, '_5_val': val})

# ЗАДАНИЕ 3 Функция записыват новые данные в базу
def record_new_vacancy(href_vac, vac_name, min, max, val):
    # собираем список ссылок существующих в базе вавансий
    href_list = []
    for vac in vacancies.find({}):
        href_list.append(vac['_4_href'])

    # проверяем, если есть ссылка новой вакансии в нашем списке - то пишем в базу и печатаем на экране, если нет, то ничего
    if href_vac not in href_list:
        record_vacancy(href_vac, vac_name, min, max, val)
        print(f'NEW !!! {vac_name}  Mинимум: {min}, Максимум: {max}, Валюта: {val}, ссылка: {href_vac} ')



# ЗАДАНИЕ 2 Функция выводит вакансии по условию зарплаты

def show_vac_condition():
    sum_vacancy = int(input('Введите сумму поиска минимальной зарплаты в вакансиях: '))
    for vac in vacancies.find({'$or':[
        {'_2_sal_min': {'$gt': sum_vacancy}},
        {'_3_sal_max': {'$gt': sum_vacancy}}]}):
        pprint(vac)


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}
link_full = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&no_magic=true&text=python&page='

page = 0

while True:
    response = requests.get(link_full + str(page), headers=headers)
    soup = bs(response.text, 'html.parser')
    block_list = soup.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    for vacancy in block_list:
        sal = None
        min = 0
        max = 0
        val = None
        vac_name = ((str(vacancy)).split('blank">')[1]).split('</a>')[0]
        href_vac = ((str(vacancy)).split('href="')[1]).split('" target="')[0]
        site_name = (((str(vacancy)).split('href="')[1]).split('" target="')[0]).split('/vac')[0]
        try:
            salary = ((str(vacancy)).split('compensation">')[1]).split('</span>')[0]
            spl_salary = salary.split(' ')
            if len(spl_salary) == 3 and spl_salary[0] == 'от':
                min = spl_salary[1].replace(u'\xa0', '')
                max = 0
                val = spl_salary[2]
            elif len(spl_salary) == 3 and spl_salary[0] == 'до':
                min = 0
                max = spl_salary[1].replace(u'\xa0', '')
                val = spl_salary[2]
            elif len(spl_salary) == 2:
                summm = spl_salary[0]
                sum_spl = summm.split('-')
                min = sum_spl[0].replace(u'\xa0', '')
                max = sum_spl[1].replace(u'\xa0', '')
                val = spl_salary[1]
            else:
                print(0)
        except:
            sal = None

        #print(f'{vac_name} {sal} Mинимум: {min}, Максимум: {max}, Валюта: {val}, ссылка: {href_vac} сайт:{site_name} ')

        # вот тут происходит выбор функции
        if variant_record == 1:
            record_vacancy(href_vac, vac_name, min, max, val)
        else:
            record_new_vacancy(href_vac, vac_name, min, max, val)


    page +=1

    button = soup.findAll('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})

    if button == []:
        break

print('\n****** загрузка в базу завершена ****** \n')

show_vac_condition()






