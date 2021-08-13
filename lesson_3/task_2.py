'''2. Написать функцию, которая производит поиск и выводит
на экран вакансии с заработной платой больше введённой суммы.'''
from pymongo import MongoClient

#подключаемся к базе mongo
client = MongoClient('127.0.0.1', 27017)
db = client['hh_ru']
hh_python = db.hh_python

val = int(input('введите значение зарплаты'))
for item in hh_python.find({'$or': [{"salary_max": {'$gt': val}}, {"salary_min": {'$gt': val}}]}):
    print(item)