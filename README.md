### Локальный запуск:
- Установите и активируйте виртуальное окружение
```
python -m venv venv
venv/scripts/activate
```
- Установите зависимости из файла requirements.txt (из директории friends_backend)
```
pip install -r requirements.txt
```
- В settings заменить данные бд на свои
- Выполнить миграции:
```
python manage.py migrate
```
- Запустить сервер:
```
python manage.py runserver
```
### Запуск в контейнерах:
- В директории infra создать .env файл и заполнить его данными, например:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
- В директории infra выполнить команду:
```
docker-compose up -d
```
- Выполнить миграции командой:
```
docker-compose exec backend python manage.py migrate
```
- Собрать статику командой:
```
docker-compose exec backend python manage.py collectstatic --noinput
```
- Cоздать суперпользователя командой:
```
docker-compose exec backend python manage.py createsuperuser
```

- Сервер будет доступен по адресу:
 - http://localhost/

- Спецификация API доступна по адресу:
 - http://localhost/redoc/


### Пример запросов при работе через докер:
- Для простоты тестирования лучше создать через админку второго пользователя, и там же делать запросы в дружбу, чтобы не переключаться между двумя пользователями.
- Также создать пользователя можно POST запросом на эндпоинт http://localhost/api/users/
- В дальнейшем для доступа к эндпоинтам потребуется передавать токен, поэтому я тестировал через postman, для простоты использования.
- Получить токен можно POST запросом на эндпоинт http://localhost/api/auth/token/login/
- Делая POST запрос на эндпоинт http://localhost/api/users/{username}/add_to_friends/ мы отправляем пользователю заявку в друзья.
- Он может принять её отправив PATCH запрос на эндпоинт http://localhost/api/friends/{username}/approve_request/
или отклонить отправив DELETE запрос на эндпоинт http://localhost/api/friends/{username}/decline_request/
- Если пользователь 1 принимает заявку пользователя 2, сразу создаётся обратная связь, ипользователь 2 добавляет в друзья пользователя 1. Если они оба кинут друг другу заявки в друзья, сработает сигнал, и они также станут друзьями.
- Если пользователь отправит DELETE запрос на эндпоинт http://localhost/api/friends/{username}/, сработает сигнал, и они удалятся из друзей друг у друга.