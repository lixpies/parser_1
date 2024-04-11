from bs4 import BeautifulSoup as BS
import requests
from PIL import Image
from io import BytesIO
import time
import pymysql
import os

# конектимся к базе
try:
    connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            database='parser',
            cursorclass=pymysql.cursors.DictCursor
    )
    print("Успешно подключился")

# выводим ошибку
except Exception as ex:
    print("Нихера не получилось, потому что:")
    print(ex)
try:
    # создаю таблицу
    with connection.cursor() as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS images (id INT AUTO_INCREMENT PRIMARY KEY, path TEXT, author TEXT, weight TEXT)''')
        print("Таблица images создалась успешно!")
except Exception as ex:
    print("Таблицу создал")

# задаю диапазон страниц, подключаю ссылку, скармливаю библиотеке содержимое ссылки
for i in range(1,2):
    url = f'https://auto.goodfon.ru/index-{i}.html'
    r = requests.get(url)
    html = BS(r.content, 'html.parser')

    # указываю путь до нужного мне контейнера на самой страничке
    for el in html.select(".wallpapers > .wallpapers__item"):
        title = el.contents[0].contents[0].contents[1].attrs['src']
        author = el.contents[0].contents[1].contents[0].attrs['title']

        # обращаюсь к ссылке на картинку, делаю проверку на ответ страницы по статусу
        response = requests.get(title)
        if response.status_code == 200:

            # открываю картинку, чтобы перезаписать
            img = Image.open(BytesIO(response.content))

            # забираю из ссылки на картинку нужное мне название и показываю что забрал
            image_name = title.rsplit('/', 1)[-1].split('.')[0]
            print(image_name)

            # получаем размер изображения (я не знаю почему длина, так в гугле было для .webp)
            file_size = len(response.content)
            print(f"Размер файла: {file_size} байт")

            # получаем размер файла
            width, height = img.size
            print(f"Размер изображения: {width}x{height}")

            # меняем размер
            new_img = img.resize((300, 300))

            # пытаемся сохранить фото в нужном формате
            new_img.save(f'photo/{image_name}.jpg', formats='jpg')
            print("Изображение успешно сохранено в формате .jpg")
            img_jpg = new_img.save
        else:
            print("Ошибка при загрузке изображения")
            img.load()
        # вывожу ссылку, просто так, чтобы видеть
        print(title)

        # указываем путь до папки, мб пригодится ()
        folder_path = './photo'
        # берём список фото
        files = os.listdir(folder_path)
        # загружаем данные в таблицу
        cursor = connection.cursor()
        file_path = os.path.abspath('./photo' + image_name + '.jpg')
        try:
            sql = ('''INSERT INTO `images` (path, author, weight) VALUES (%s,%s,%s)''')
            cursor.execute(sql, (file_path, author, str(file_size)))
            connection.commit()  # Выполнение коммита после каждой вставки иначе не работает, не удалять!
            print("Данные успешно добавлены в базу")
        except Exception as ex:
            print("Ошибка при добавлении данных в базу:", ex)

# закрываем соединение с базой
connection.commit()
connection.close()
























