![Test and push to Docker Hub](https://github.com/mityasun/yatube/actions/workflows/yatube_workflow.yml/badge.svg)

## Проект Yatube - социальная сеть для авторов.

***Здесь вы можете создавать свои записи, добавлять их в сообщества, подписываться на авторов и комментировать их записи.***

### Возможности проекта:
- Регистрация с расширенным профилем и управление им (переопределение модели User с помощью AbstractUser).
- Публикация записей с изображениями.
- Публикация записей в сообщества.
- Комментарии к записям других авторов.
- Подписка на других авторов.
- Лента с записями, на которых оформлена подписка.
- Template tags, отображающие самые обсуждаемые записи, последние записи и пр.
- Для проекта написаны тесты Unittest.

### Возможности API:
- Получение, создание, обновление, удаление записей.
- Получение, создание, обновление, удаление комментариев.
- Получение списка сообществ и их информации.
- Получение списка подписок и создание подписки на авторов.
- Получение, обновление и проверка токена авторизации (JWT).

Подробней про API [по ссылке](http://localhost/api/v1/redoc/)<br>
<sub>Ссылка откроется после развертывания проекта.</sub>
<br>

### Технологии
![Python](https://img.shields.io/badge/Python-3.9.8-%23254F72?style=for-the-badge&logo=python&logoColor=yellow&labelColor=254f72)
![Django](https://img.shields.io/badge/Django-2.2.28-0C4B33?style=for-the-badge&logo=django&logoColor=white&labelColor=0C4B33)
![Django](https://img.shields.io/badge/Django%20REST-3.12.4-802D2D?style=for-the-badge&logo=django&logoColor=white&labelColor=802D2D)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-712CF9?style=for-the-badge&logo=bootstrap&logoColor=white&labelColor=712CF9)
![Jquery](https://img.shields.io/badge/Jquery-3.6.0.min.js-0769AD?style=for-the-badge&logo=jquery&logoColor=white&labelColor=0769AD)

### Как запустить проект:

Клонировать репозиторий и перейти в него в терминале:

```
git clone https://github.com/mityasun/yatube.git
```

Перейдите в директорию:
```
cd yatube/yatube/
```

Cоздать образ из Docker файла:

```
docker build -t yatube .
```

Перейдите в директорию с настройками Docker-compose:

```
cd yatube/infra/
```

Создать файл .env в этой директории пропишите в нем настройки БД:

```
SECRET_KEY=*Секретный ключ Django*
DEBUG=*False для прода и True для тестов*
ALLOWED_HOSTS=*Список разрешенных хостов*
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