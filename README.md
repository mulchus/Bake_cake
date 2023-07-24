# Сайт производства тортов BakeCake

Это сайт сети роизводства тортов BakeCake. Здесь можно заказать превосходные торты с доставкой на дом.
![site](https://github.com/mulchus/Bake_cake/assets/111083714/a9e041ae-fdc8-463b-9f8a-3ccfb08cdf44)


## Переменные окружения
Часть настроек проекта берётся из переменных окружения.  
Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ = значение`:  
- `BITLY_TOKEN` - [Как получить](https://dev.bitly.com/docs/getting-started/authentication).  

определить данные своего почтового сервера и почтового ящика (пример):  
- `EMAIL_HOST` = 'smtp.yandex.ru'  
- `EMAIL_PORT` = 465  
- `EMAIL_USE_TLS` = False  
- `EMAIL_USE_SSL` = True  
- `EMAIL_HOST_USER` = 'bakecake@yandex.ru'  
- `EMAIL_HOST_PASSWORD` = 'password'  

настроить Django:  
- `SECRET_KEY` — секретный ключ проекта в Django. [Как получить?](https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django).   
- `DEBUG` — дебаг-режим. Поставьте `True`, чтобы увидеть отладочную информацию в случае ошибки.  
- `ALLOWED_HOSTS` — (адрес сайта без протокола HTTPS). [Документация Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).  
- `CSRF_TRUSTED_ORIGINS` = (полный адрес сайта, включая протокол HTTPS)
  
следующие настройки менять не требуется, значения проставлены для деплоя:  
- `STATIC_ROOT = assets`  
- `SECURE_HSTS_SECONDS = 10`  
- `SESSION_COOKIE_SECURE = True`  
- `CSRF_COOKIE_SECURE = True`  
- `SECURE_HSTS_PRELOAD = True`  
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`  
- `SECURE_SSL_REDIRECT = True`  
[Документация по настройкам Django Deployment checklist](https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/).  


## Установка и запуск
Для запуска у вас уже должен быть установлен Python не ниже 3-й версии.  

- Скачайте код: `git clone https://github.com/mulchus/Bake_cake.git`
- Создайте файл с переменными окружения, активируйте виртуальное окружение: 
    `python -m venv venv`  
    - Windows: `.\venv\Scripts\activate`  
    - MacOS/Linux: `source venv/bin/activate`  
- Установите зависимости: `pip install -r requirements.txt`  
- Создайте файл базы данных и примените все миграции: `python manage.py migrate`  
- Запустите сервер: `python manage.py runserver`


## Администрирование
- Для регистрации администратора сайта введите: `python manage.py createsuperuser`,  
    после чего введите выбранный вами логин, e-mail и пароль администратора (2 раза).  
    При вводе пароля символы не отображаются. Ввод завершается нажатием Enter.  
- Перейдите по адресу сайта, указанному выше в `ALLOWED_HOSTS`
- Используйте данные для авторизации (Username: Password:, введенные ранее)


## Панель администратора
![admin-panel](https://github.com/mulchus/Bake_cake/assets/111083714/43fb6c5b-a39f-41a0-ab3b-fae76cab3a43)


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
