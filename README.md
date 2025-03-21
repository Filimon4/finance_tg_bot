# Установка

```
python -m venv venv

./venv/Scripts/activate

pip install -r requirements.txt
```
# Запуск
```py
python ./src/index.py
```

# Архитектура проекта

## Core

В папке src/core лежат глобальные объекты для бота, которые непосредственно относятся к боту.
Такое решение позволит быстро обрщаятся к объектам бота из любой части кода. В дальнейшем они будут расширятся под нужный функционал.

## Routes

Для бота нужны рауты по которым он будет слушать сообщения, для этого есть папка routes. Файлы этой папки с названиям routes загружаются автоматически при старке бота.

Загрузка происходит вот таким образом:

```py
from utils.loadModulesByRegex import load_modules_by_regex
load_modules_by_regex(os.path.dirname('src/routes'), r'routes.py')
```

Поэтому для всех раутов создаём файл routes.py

## IDE

Для проекта есть кастомный настройки vs code, которые просто скрывают **pycache** файлы. Без них намного удобнее работать. Поэтмоу лучше пользуйтесь vs code ;D

## Форматирование кода

Что бы отформатировать код нужно запустить команду

```cmd
black .
```

## Миграции к бд
Генерация миграции
```cmd
alembic revision --autogenerate -m "Your changes"
```
Исполненеи мигарации
```cmd
alembic upgrade head
```

## Fastify Server
Что запустить севрер для миниапы нужно запустить команду из папки ./src/serverBot
```cmd
uvicorn index:app --reload --port 9000
```