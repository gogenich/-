'''1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать
функцию, записывающую собранные вакансии в созданную БД.'''
import pandas as pd
from pymongo import MongoClient

#подключаемся к базе mongo
client = MongoClient('127.0.0.1', 27017)
#создаем бд
db = client['hh_ru']
# читаем датафрейм
data_hh = pd.read_csv("rezult_hh.csv", sep=";")
# создаем коллекцию
hh_python = db.hh_python

#добавляем данные в коллекцию
for i in range(len(data_hh)):
    db.hh_python.insert_one({
        'id': i,
        "name_job": data_hh['name'][i],
        "link_job": data_hh['link'][i],
        "salary_min": int(data_hh['salary_min'][i]),
        "salary_max": int(data_hh['salary_max'][i]),
        "salary_valut": data_hh['salary_valut'][i]})