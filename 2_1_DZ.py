from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pprint import pprint

# проект предусматривал созранение в EXCEL  методами pd, но не хочется затягивать с сдачей

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}
link_full = 'https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&no_magic=true&text=python&page='

page = 0

while True:
    response = requests.get(link_full + str(page), headers=headers)
    soup = bs(response.text, 'html.parser')
    block_list = soup.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    for vacancy in block_list:
        sal = ''
        min = 'нет'
        max = 'нет'
        val = 'нет'
        vac_name = ((str(vacancy)).split('blank">')[1]).split('</a>')[0]
        href_vac = ((str(vacancy)).split('href="')[1]).split('" target="')[0]
        site_name = (((str(vacancy)).split('href="')[1]).split('" target="')[0]).split('/vac')[0]
        try:
            salary = ((str(vacancy)).split('compensation">')[1]).split('</span>')[0]
            spl_salary = salary.split(' ')
            if len(spl_salary) == 3 and spl_salary[0] == 'от':
                min = spl_salary[1]
                max = 'нет'
                val = spl_salary[2]
            elif len(spl_salary) == 3 and spl_salary[0] == 'до':
                min = 'нет'
                max = spl_salary[1]
                val = spl_salary[2]
            elif len(spl_salary) == 2:
                summm = spl_salary[0]
                sum_spl = summm.split('-')
                min = sum_spl[0]
                max = sum_spl[1]
                val = spl_salary[1]
            else:
                print(0)
        except:
            sal = 'без указания з/п'

        print(f'{vac_name} {sal} Mинимум: {min}, Максимум: {max}, Валюта: {val}, ссылка: {href_vac} сайт:{site_name} ')
    page +=1

    button = soup.findAll('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})

    if button == []:
        break


