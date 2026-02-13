# Task Management API

REST API для задач на FastAPI + PostgreSQL.  
CRUD задач, JWT авторизация, Alembic миграции, Docker.

## Быстрый старт

1. Клонируйте репозиторий:

```bash
git clone https://github.com/твой-логин/task-manager-api.git
cd task-manager-api

2. Создайте .env:

cp .env.example .env

3. Запустите:

docker-compose up --build

4. Swagger UI:

http://localhost:8000/docs

Переменные окружения (.env.example)

POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=tasks_db
DB_HOST=db
SECRET_KEY=supersecretkey

Миграции

docker-compose run app alembic upgrade head