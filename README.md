# DRF Homework

DRF Homework - это проект на Django REST Framework (DRF), демонстрирующий операции CRUD с курсами и уроками.

## Установка

1. Клонируйте репозиторий на ваш локальный компьютер:

git clone https://github.com/EvgeniyKhan/drfhomework.git

markdown
Копировать код

2. Перейдите в папку проекта:

cd drfhomework

markdown
Копировать код

3. Создайте виртуальное окружение и активируйте его:

python3 -m venv env
source env/bin/activate

markdown
Копировать код

4. Установите зависимости:

pip install -r requirements.txt

markdown
Копировать код

5. Настройте базу данных:

python manage.py migrate

markdown
Копировать код

6. Создайте суперпользователя для доступа к админке:

python manage.py createsuperuser

markdown
Копировать код

7. Запустите сервер разработки:

python manage.py runserver

markdown
Копировать код

8. Откройте браузер и перейдите по адресу `http://localhost:8000/` для доступа к API.

## API Endpoints

### Уроки (Lessons)

- `/lesson/create/`: Создание нового урока.
- `/lesson/`: Список всех уроков.
- `/lesson/view/<int:pk>/`: Просмотр конкретного урока.
- `/lesson/update/<int:pk>/`: Обновление конкретного урока.
- `/lesson/delete/<int:pk>/`: Удаление конкретного урока.

### Курсы (Courses)

- `/course/create/`: Создание нового курса.
- `/course/list/<int:pk>/`: Список всех курсов.

### Подписки (Subscriptions)

- `/subscriptions/`: Список подписок.

## Использование

1. Создайте новый урок, отправив POST запрос на `/lesson/create/` с необходимыми данными.
2. Получайте, обновляйте или удаляйте уроки через соответствующие эндпоинты API.
3. Создайте новый курс через `/course/create/` и просматривайте список курсов через `/course/list/<int:pk>/`.
4. Просматривайте список подписок через `/subscriptions/`.

## Дополнительная информация

- Этот проект использует Django REST Framework для создания API.
- Некоторые эндпоинты могут требовать аутентификации. Рекомендуется использовать токенную аутентификацию или аутентификацию по сессии.

## Внесение вклада

Если у вас есть предложения, найдены ошибки или вы хотите внести свой вклад, пожалуйста, создайте Issue или отправьте Pull Request на GitHub.

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.