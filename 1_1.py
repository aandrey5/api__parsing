import requests
import json

i = 1


def sm():
    print('=' * 60)


# здесь вставить пользователя
user_contr = 'apple'
result = requests.get(f'https://api.github.com/users/{user_contr}/repos')
data = result.json()

sm()
print(f'Список открытых репозиториев пользователя {user_contr}')
sm()

for el in data:
    print(i, el['name'])
    i += 1

sm()
print(f'Записываем исходные данные в файл repo.json')
sm()

with open("repo.json", "w") as write_f:
    json.dump(data, write_f, indent=1)
