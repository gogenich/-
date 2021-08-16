"""1. Написать приложение, которое собирает основные новости с сайтов

https://news.mail.ru,
https://lenta.ru,
https://yandex.ru/news.
Для парсинга использовать XPath. Структура данных должна содержать:

название источника;
наименование новости;
ссылку на новость;
дата публикации.
2. Сложить собранные данные в БД"""

#https://lenta.ru/

from lxml import html
import requests
from datetime import date
from pymongo import MongoClient

#подключаемся к источнику и находим нужные классы
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
url = 'https://lenta.ru/'
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
news = dom.xpath("//div[@class = 'row js-content']")
news_1 = news[1].xpath(".//div[@class = 'item article']")
news_2 = news[1].xpath(".//div[@class = 'item news b-tabloid__topic_news']")

# переменные в которые сохраняем данные
title = []
link = []
date_new = []
source = []

# добываем данные
for new in news_1:
    title.append(new.xpath(".//span[@class = 'rightcol']/text()")[0])
    link.append(new.xpath(".//a[@class = 'titles']/@href")[0])
    date_new.append(new.xpath(".//span[@class = 'g-date item__date']/text()")[0])
for new_2 in news_2:
    title.append(new_2.xpath(".//h3[@class = 'card-title']/text()")[0])
    link.append(new_2.xpath(".//a[@class = 'titles']/@href")[0])
    date_new.append(new_2.xpath(".//span[@class = 'g-date item__date']/text()")[0])

#подключаемся к базе mongo
client = MongoClient('127.0.0.1', 27017)
#создаем бд
db = client['lenta_ru']
lenta_ru = db.lenta_ru

# немного расчесываем данные и записываем их в монго(проверяя нет ли похожих ссылок)
for i in range(len(title)):
    title[i] = title[i].replace('\xa0', ' ')
    if link[i][0] == '/':
        link[i] = url + link[i]
    source.append(link[i].split('/')[2])
    if date_new[i] == 'Сегодня':
        date_new[i] = str(date.today())
    links = [el['link_new'] for el in db.lenta_ru.find({})]
    if links.count(link[i]) > 0:
        continue
    lenta_ru.insert_one({"title_new": title[i], "link_new": link[i], "data_new": date_new[i], "sourse": source[i]})

