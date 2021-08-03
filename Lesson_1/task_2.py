import requests
import json

url = ' https://faq.whatsapp.com/en/smba'

#user agent
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'}

data = requests.get(url, headers=headers).json()
print(data)