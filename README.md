# FoodGram - Продуктовый помощник

**Описание**
> На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
## **Стек технологий**
![CI](https://img.shields.io/badge/Django%20Rest%20Framework-3.12.4-success)
![CI](https://img.shields.io/badge/Django-3.2.13-green)
![CI](https://img.shields.io/badge/Requests-2.26.0-yellow)
![CI](https://img.shields.io/badge/Python-v3.8-blue)
![CI](https://img.shields.io/badge/-Djoser-yellowgreen)
![CI](https://img.shields.io/badge/-Nginx-blueviolet)
![CI](https://img.shields.io/badge/-Docker-blueviolet)
![CI](https://img.shields.io/badge/-Linux-red)
## **Стек технологий**
**Запуск проекта:**

**Клонировать репозиторий [foodgram](https://github.com/Aleksandr-Meshkov/foodgram-project-react) и перейти в него в командной строке:**

**Подготовьте сервер:**

```
    scp docker-compose.yml <username>@<host>:/home/<username>/
    scp nginx.conf <username>@<host>:/home/<username>/
    scp .env <username>@<host>:/home/<username>/
```
**Установите docker и docker-compose:**
```
    sudo apt install docker.io 
    sudo apt install docker-compose
```
**Создайте суперюзера, сделайте миграции соберите статику:**
```
    sudo docker-compose exec backend python manage.py migrate
    sudo docker-compose exec backend python manage.py createsuperuser
    sudo docker-compose exec backend python manage.py collectstatic --no-input
```

**Адрес сервера**
```
    http://84.201.160.215/recipes
```

![CI](https://github.com/Aleksandr-Meshkov/foodgram-project-react/actions/workflows/main.yml/badge.svg)
