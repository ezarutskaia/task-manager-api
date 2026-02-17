# Task Management API

REST API для управления задачами с JWT-авторизацией.
Стек: FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker.

## Быстрый старт

1. Клонируйте репозиторий:

```bash
git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api
```

2. Запустите проект:

```bash
docker-compose up --build
```

3. Создайте и примените миграции (в отдельном терминале):

```bash
docker-compose exec app alembic revision --autogenerate -m "initial"
docker-compose exec app alembic upgrade head
```

4. API готово к работе:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Переменные окружения

Значения по умолчанию уже заданы в коде, для разработки дополнительная настройка не требуется.
Для продакшена задайте переменные в `docker-compose.yml` или через `.env`:

| Переменная | По умолчанию | Описание |
|---|---|---|
| `POSTGRES_USER` | `user` | Пользователь БД |
| `POSTGRES_PASSWORD` | `password` | Пароль БД |
| `POSTGRES_DB` | `tasks_db` | Имя базы данных |
| `DB_HOST` | `db` | Хост БД (имя сервиса в Docker) |
| `SECRET_KEY` | `dev-secret-key` | Секретный ключ для подписи JWT-токенов |

## API-эндпоинты

### Авторизация

| Метод | URL | Описание | Авторизация |
|---|---|---|---|
| POST | `/register` | Регистрация нового пользователя | Нет |
| POST | `/login` | Вход, получение JWT-токена | Нет |

### Задачи

Все эндпоинты задач требуют JWT-токен в заголовке: `Authorization: Bearer <токен>`

| Метод | URL | Описание |
|---|---|---|
| POST | `/tasks/` | Создать задачу |
| GET | `/tasks/` | Получить список своих задач |
| GET | `/tasks/{id}` | Получить задачу по ID |
| PATCH | `/tasks/{id}` | Обновить задачу |
| DELETE | `/tasks/{id}` | Удалить задачу |

## Примеры запросов

### Регистрация

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "anna", "email": "anna@test.com", "password": "123456"}'
```

Ответ:
```json
{"id": 1, "username": "anna", "email": "anna@test.com"}
```

### Логин

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "anna@test.com", "password": "123456"}'
```

Ответ:
```json
{"access_token": "eyJhbGciOi...", "token_type": "bearer"}
```

### Создание задачи

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <токен>" \
  -d '{"title": "Моя задача", "description": "Описание"}'
```

### Получение своих задач

```bash
curl http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <токен>"
```

## Миграции (Alembic)

```bash
# Применить все миграции
docker-compose exec app alembic upgrade head

# Откатить последнюю миграцию
docker-compose exec app alembic downgrade -1

# Посмотреть текущую ревизию
docker-compose exec app alembic current

# Посмотреть историю миграций
docker-compose exec app alembic history

# Создать новую миграцию после изменения моделей
docker-compose exec app alembic revision --autogenerate -m "описание изменений"
```

## Структура проекта

```
.
├── app/
│   ├── __init__.py          # Инициализация пакета
│   ├── main.py              # Точка входа, эндпоинты FastAPI
│   ├── database.py          # Подключение к PostgreSQL
│   ├── models.py            # SQLAlchemy-модели (Task, User)
│   ├── schemas.py           # Pydantic-схемы валидации
│   ├── crud.py              # CRUD-операции с БД
│   ├── dependencies.py      # JWT-авторизация (get_current_user)
│   └── exceptions.py        # HTTP-ошибки
├── migrations/
│   ├── env.py               # Конфигурация Alembic
│   └── versions/            # Файлы миграций
├── alembic.ini              # Настройки Alembic
├── docker-compose.yml       # Docker Compose (app + PostgreSQL)
├── Dockerfile               # Образ приложения
├── requirements.txt         # Python-зависимости
└── README.md
```
