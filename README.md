### Опиание проекта.
Сайт Foodgram, «Продуктовый помощник». Это онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Проект доступен по ссылкам:

```
- http://158.160.73.139/
- http://158.160.73.139/admin/
- http://158.160.73.139/api/docs/
```

## Учетная запись администратора:

```
- логин: review
- почта:review@admin.ru 
- пароль: review1admin
```

Foodgram - проект позволяет:

- Просматривать рецепты
- Добавлять рецепты в избранное
- Добавлять рецепты в список покупок
- Создавать, удалять и редактировать собственные рецепты
- Скачивать список покупок

## Инструкции по установке
***- Клонируйте репозиторий:***
```
git clone git@github.com:PavelDubanenko/foodgram-project-react.git
```

***- Установите и активируйте виртуальное окружение:***
- для MacOS
```
python3 -m venv venv
```
- для Windows
```
python -m venv venv
source venv/bin/activate
source venv/Scripts/activate
```

***- Установите зависимости из файла requirements.txt:***
```
pip install -r requirements.txt
```

***- Примените миграции:***
```
python manage.py migrate
```

***- В папке с файлом manage.py выполните команду для запуска локально:***
```
python manage.py runserver
```
***- Локально Документация доступна по адресу:***
```
http://127.0.0.1/api/docs/
```

### Собираем контейнерыы:

Из папки infra/ разверните контейнеры при помощи docker-compose:
```
docker-compose up -d --build
```
Выполните миграции:
```
docker-compose exec backend python manage.py migrate
```
Создайте суперпользователя:
```
winpty docker-compose exec backend python manage.py createsuperuser
```
Соберите статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
Наполните базу данных ингредиентами и тегами. Выполняйте команду из дериктории где находится файл manage.py:
```
docker-compose exec backend python manage.py load_data

```
Остановка проекта:
```
docker-compose down
```

### Подготовка к запуску проекта на удаленном сервере

Cоздать и заполнить .env файл в директории infra
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
TOKEN=252132607137
ALLOWED_HOSTS=*
```

### Связаться с автором
```
https://vk.com/id331954776
```

### Список использованных библиотек:
```
asgiref==3.6.0
certifi==2022.12.7
cffi==1.15.1
charset-normalizer==3.0.1
coreapi==2.3.3
coreschema==0.0.4
cryptography==39.0.0
defusedxml==0.7.1
Django==4.1.6
django-colorfield==0.8.0
django-filter==22.1
django-templated-mail==1.1.1
djangorestframework==3.14.0
djangorestframework-simplejwt==4.8.0
djoser==2.1.0
flake8==6.0.0
gunicorn==20.1.0
idna==3.4
install==1.3.5
itypes==1.2.0
Jinja2==3.1.2
MarkupSafe==2.1.2
mccabe==0.7.0
oauthlib==3.2.2
Pillow==9.4.0
psycopg2-binary==2.9.5
pycodestyle==2.10.0
pycparser==2.21
pyflakes==3.0.1
PyJWT==2.6.0
python-dotenv==0.21.1
python3-openid==3.2.0
pytz==2022.7.1
requests==2.28.2
requests-oauthlib==1.3.1
six==1.16.0
social-auth-app-django==4.0.0
social-auth-core==4.3.0
sqlparse==0.4.3
tzdata==2022.7
uritemplate==4.1.1
urllib3==1.26.14
webcolors==1.12
```
