### Как запустить проект:

# praktikum_new_diplom
![example branch parameter](https://github.com/exusainov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:exusainov/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:

```
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

* python manage.py migrate

Создать суперпользователя:
​
```
python manage.py createsuperuser
```

Заполнение ингредиентов и тегов в базу:
```
python manage.py load_ingrs
python manage.py load_tags
```

Запустить проект:

```
python manage.py runserver
```
# Шаблон наполнение .env

Создать файл .env на основе .env.example в папке infra/:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```

# Запуск docker-compose. Взлетаем!

Пересоберите контейнеры и запустите их:


* docker-compose up -d --build

Выполните по очереди команды:

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input
```

Теперь проект доступен по адресу: http://localhost/


# Технологии
​
Python3, Django, HTTP, Django Rest Framework, PostgreSQL, Docker, YandexCloud
​

# Авторы
​
- Хусаинов Евгений Маратович (Exusainov@yandex.com)
​- IP Адрес http://exusainov.ddns.net/  IP - 158.160.1.215
