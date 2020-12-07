import requests

#NASA запрос астероидов

def sm():
    print('=' * 80)
sm()
print('СМОТРИМ АСТЕРОИДЫ РЯДОМ С ЗЕМЛЕЙ ЗА ВЫБРАННЫЙ ДЕНЬ В ПЕРИОДЕ')
sm()

#входные параметры
start_date = '2020-12-01'
end_date = '2020-12-07'
current_date = '2020-12-05'
sm()
print(f'Смотрим за период от {start_date} до {end_date} на дату {current_date}')
sm()

# ключ авторизации
api_key = '6yW9hlFfGsbewRlypm4yieqSkgPvnoRk5QfIU0qc'

#запрос
result = requests.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}')
data = result.json()

#выводим список
for el in data:
    for el in data['near_earth_objects'][current_date]:
        print('ID =',el['id'], ' | имя астероида:',el['name'])



#ТЕСТОВЫЕ СТРОКИ
#for el in result:
   # print((str(el).replace("b'", "")).replace("'", ""))

  #print(data['near_earth_objects']['2020-12-05'][1])
