'''Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность) с сайтов
HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать
несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:

    Наименование вакансии.
    Предлагаемую зарплату (отдельно минимальную и максимальную).
    Ссылку на саму вакансию.
    Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно
вывести с помощью dataFrame через pandas. Сохраните в json либо csv.'''
#https://arkhangelsk.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

#функция для преобразования зарплаты
def transform(text):
    min = []
    max = []
    val = []
    for i in text:
        if i == '':
            min.append(0)
            max.append(0)
            val.append(0)
        if i[0:1].isdigit():
            i = i.replace('\u202f', '')
            res = i.split(' ')
            min.append(int(res[0]))
            max.append(int(res[2]))
            val.append(res[3])
        if i[0:2] == 'до':
            i = i.replace('\u202f', '')
            res = i.split(' ')
            min.append(0)
            max.append(int(res[1]))
            val.append(res[2])
        if i[0:2] == 'от':
            i = i.replace('\u202f', '')
            res = i.split(' ')
            max.append(0)
            min.append(int(res[1]))
            val.append(res[2])

    return {'min': min,
            'max': max,
            'val': val}


headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'}
url = 'https://arkhangelsk.hh.ru/search/vacancy'
param = {
    'area': '',
    'items_on_page': 20, #параметр для полного вывода профессий
    'fromSearchLine': 'true',
    'st': 'searchVacancy',
    'text': 'Python',
    'from': 'suggest_post',
    'page': '0'

}

#запрос для получения кода страници
respons = requests.get(url, params=param, headers=headers)
soup = bs(respons.text, 'html5lib')

#извлекаем максимальное колво страниц
page_resp = soup.find('div', {'data-qa': 'pager-block'})
children = list(page_resp.children)
max_page = int(children[1].text[3:])

# создаём переменные, куда будем сохранять данные
name = []
link = []
salary = []

# проходимся по каждой странице
for n in range(max_page):
    param = {
        'area': '',
        'items_on_page': 20,
        'fromSearchLine': 'true',
        'st': 'searchVacancy',
        'text': 'Python',
        'from': 'suggest_post',
        'page': n
    }
    # запрос на страницу
    respons = requests.get(url, params=param, headers=headers)
    soup = bs(respons.text, 'html5lib')
    elems = soup.find_all('div', {'class': 'vacancy-serp-item'})

    # извлекаем информацию
    for i in elems:
        info = i.find('div', {'class': 'vacancy-serp-item__info'})
        name.append(info.getText())

        sidebar = i.find('div', {'class': 'vacancy-serp-item__sidebar'})
        salary.append(sidebar.getText())

        elem_url = info.find('a', {'class': 'bloko-link'}).get('href')
        link.append(elem_url)

# преобразуем зарплату
salary = transform(salary)

#вывод информации
rezult_hh = {
    'name': name,
    'link': link,
    'salary_min': salary['min'],
    'salary_max': salary['max'],
    'salary_valut': salary['val']
}
rezult_hh = pd.DataFrame(rezult_hh)
rezult_hh.to_csv("rezult_hh.csv", sep=";", index=False)


