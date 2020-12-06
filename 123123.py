import requests

headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
'Authorization' : 'Basic cG9zdG1hbjpwYXNzd29yZA=='
}

req = requests.get('https://postman-echo.com/basic-auth', headers=headers)


print('Заголовки \n', req.headers)

print('Ответ \n', req.text)