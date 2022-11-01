## Проект Yatube - социальная сеть для авторов.

***Здесь вы можете создавать свои записи, добавлять их в сообщества, подписываться на авторов и комментировать их записи.***

### Возможности проекта:
- Регистрация с расширенным профилем и управление им (переопределение модели User с помощью AbstractUser).
- Публикация записей с изображениями.
- Публикация записей в сообщества.
- Комментарии к записям других авторов.
- Подписка на других авторов.
- Лента с записями, на которых оформлена подписка.
- Пользовательские теги, отображающие самые обсуждаемые записи, последние записи и т.д.
- Для проекта написаны тесты Unittest.

### Технологии
- Python 3.9.8<br>
- Django 2.2.28<br>
- Bootstrap<br>
- Jquery<br>

### Как запустить проект:

Клонировать репозиторий и перейти в него в терминале:

```
git clone https://github.com/mityasun/yatube.git
```

Перейдите в директорию:
```
cd yatube/yatube/
```

Создать файл .env в этой директории пропишите в нем:

```
SECRET_KEY=*Секретный ключ Django*
```

Cоздать образ из Docker файла:

```
docker build -t yatube .
```

Перейдите в директорию с настройками Docker-compose:

```
cd yatube/docker-compose/
```

Создать файл .env в этой директории пропишите в нем настройки БД:

```
DB_NAME=*Имя БД*
POSTGRES_USER=*Имя пользователя БД*
POSTGRES_PASSWORD=*Пароль пользователя БД*
DB_HOST=db
DB_PORT=5432
```

Соберите образ из файла Docker-compose:
```
docker-compose up -d --build
```

Примените миграции:

```
docker-compose exec web python manage.py migrate
```

Соберите статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Заполнить базу данными из копии:

```
docker-compose exec web python manage.py loaddata fixtures.json
```

Создайте суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

<br>

### Автор проекта:
Петухов Артем [Github](https://github.com/mityasun)