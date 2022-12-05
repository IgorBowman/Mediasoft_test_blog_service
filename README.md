
### Описание:

* Документация с помощью swagger ```/swagger```
* Создать блог (POST```/api/blogs```)
* Добавить в свой блог авторов (PATCH```/api/blogs/{blog_id}/add-authors```)
* Публиковать в блог посты (POST```/api/posts```)
* Добавить комментарий к посту (POST```/api/posts/{post_id}/add-comment```)
* Добавлять блог в мои подписки (PATCH```/api/blogs/{blog_id}/subscribe```)
* Главная страница с N количеством постов со всех блогов (GET```/api/posts```)
* Список блогов (GET```/api/blogs```)
* Список блогов (GET```/api/blogs/{blog_id}/posts```)
* Посты опубликованные пользователем (GET```/api/posts/my```)
* Блоги на которые подписан пользователь (GET```/api/blogs/favorites```)
* CRUD на блоги и посты (GET```/api/posts/my```)

### Аутентификация/авторизация пользователя:
* Создание пользователя. Отправить username и password (POST ```/auth/sign-in```)
* Авторизация пользователя. Отправить username и password (POST ```/auth/login```), в ответе будут access и refresh токены
* Для помещения токена в blacklist отправить (POST ```/auth/token/blacklist```) с refresh токеном
* Для отправки авторизованного запроса, добавить к запросу заголовок Authorization со значением Bearer {access token}


### Подготовительные действия
* Клонировать проект ```git clone```
* Создать окружение ```pip install virtualenv ```
                       ```python3 -m venv venv``` 
                        ```venv/bin/activate```
* Установить зависимости```pip install -e requirements.txt```
* Создать БД PostgreSQL
* В файл .env.example внести необходимые настройки
* Запустить миграции командой ```python manage.py migrate```
* Создание superuser ```python manage.py createsuperuser```

### Запуск приложения
* ```python manage.py runserver```

### Запуск docker
1) Создание образа ```docker-compose build```
2) Запуск котейнера ```docker-compose up```
3) Создание супер пользователя ```docker exec -it blog_app python manage.py createsuperuser```
