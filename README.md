# Проект на Django
## Тема: Кулинарные рецепты
https://lk.neural-university.ru/lesson/840

### Для запуска выполните следующие команды:
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py seed
- python manage.py runserver

После этого откройте в браузере страницу http://127.0.0.1:8000/admin

### Запуск тестов
    coverage run manage.py test

### Просмотр степень покрытия кода тестами в консоли
    coverage report

### Просмотр степень покрытия кода тестами браузере
    coverage html
    далее нужно открыть в браузере файл ./htmlcov/index.html
