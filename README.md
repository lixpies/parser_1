# parser_1

1. Перед запуском проекта нужно установить библиотеки:

from bs4 import BeautifulSoup as BS
import requests
from PIL import Image
from io import BytesIO
import time
import pymysql
import os


2. Нужно иметь локальный сервер  Phpmyadmin
Настройки доступа выставлять в часть:

try:
    connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            database='parser',
            cursorclass=pymysql.cursors.DictCursor
    )

3. Задать количество страниц парсеру здесь:
for i in range(1,2)

4. И создать папку в проекте с названием 'photo'
