import requests
import json

#имя пользователя на гитхаб
username = 'gogenich'

#url для запроса
url = f'https://api.github.com/users/{username}/repos'

#user agent
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'}

data = requests.get(url, headers=headers).json()
with open('data.json', 'w') as out:
    json.dump(data, out)

list_repoz = [data[i]['name'] for i in range(len(data))]
print(list_repoz)

