'''1) Написать программу, которая собирает входящие письма из своего или
тестового почтового ящика и сложить данные о письмах в базу данных
(от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172!!!'''

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#подклучение драйвера
driver = webdriver.Chrome(executable_path='./chromedriver')

#делаем запрос на страничку
driver.get('https://mail.ru/')

"""вводим логин и пароль пользователя"""
login = driver.find_element_by_xpath("//input[contains(@class, 'email-input')]") #поиск поля для логина
login.send_keys('study.ai_172@mail.ru') #вводим логин
but = driver.find_element_by_xpath("//button[contains(@class, 'button svelte')]").click() #кликаем на кнопку для перехода к вводу пароля
passw = driver.find_element_by_xpath("//input[contains(@class, 'password-input')]")#ищем поле для ввода пароля
passw.send_keys('NextPassword172!!!')#вводи пароль
but = driver.find_element_by_xpath("//button[contains(@class, 'second-button')]").click()#входим в почту

"""после того как перешли к письмам, находим первое письмо и кликаем по нему"""
time.sleep(5)#задержка для прогрузки страницы
driver.find_element_by_xpath("//a[contains(@class, 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal')]").click()
time.sleep(5)

"""собираем информацию с первой странички(перевого письма) а также создаем списки для добавления данных"""
first_name = driver.find_element_by_class_name('thread__subject').text
name = ''

from_whom = []
from_whom.append(driver.find_element_by_class_name('letter-contact').text)

name_list = []
name_list.append(first_name)

data = []
data.append(driver.find_element_by_class_name('letter__date').text)

"""запускаем цикл который кликает по кнопке и собирает инфу со странички"""
while first_name != name:
    but = driver.find_elements_by_xpath("//span[contains(@class, 'button2__ico')]")
    but[9].click()
    time.sleep(0.5)
    name = driver.find_element_by_class_name('thread__subject').text
    name_list.append(name)
    from_whom.append(driver.find_element_by_class_name('letter-contact').text)
    data.append(driver.find_element_by_class_name('letter__date').text)

