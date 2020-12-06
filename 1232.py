import requests

from pprint import pprint


APIkey = 'fadab5a8fc2d58607af748579bc794c0'

city_name = 'Moscow'

call_res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={APIkey}')

data = call_res.json()

pprint(data)
#data = json.loads(call_res.text)

print(f"В городе {data['name']} температура {round((data['main']['temp'])-273.15)} градуса")