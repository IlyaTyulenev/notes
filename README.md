# Notes API

Простой асинхронный REST API сервис для управления заметками.

## Архитектура проекта

```bash
app/
  main.py                   # запуск приложения, CORS, OpenAPI, lifespan
  api/
    deps.py                 # зависимости FastAPI (DB, current user)
    routes/
      auth.py               # эндпоинты /auth: регистрация, логин
      notes.py              # эндпоинты /notes: CRUD
  core/
    config.py               # конфигурация из .env (pydantic-settings)
    security.py             # JWT, OAuth2, хеширование паролей
  db/
    base.py                 # базовая модель (Base.metadata)
    session.py              # engine, session
  models/
    user.py                 # модель User
    note.py                 # модель Note
  schemas/
    user.py                 # схемы Pydantic для auth
    note.py                 # схемы Pydantic для notes
tests/
  conftest.py               # фикстуры pytest (DB, client)
  test_notes.py             # тесты CRUD для заметок
Dockerfile
docker-compose.yml
requirements.txt
.env
README.md
```

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repo_url>
cd notes
```

### 2. Запуск через docker-compose
```bash
docker compose up --build
```

Приложение будет доступно на:

API: http://localhost:8000

Swagger UI: http://localhost:8000/docs

OpenAPI JSON: http://localhost:8000/openapi.json

## Тестирование
```bash
docker compose run --rm app pytest -q
```

## API
#### Auth

- POST /auth/register — регистрация (email, password)

- POST /auth/login — получение JWT токена (email, password)

#### Notes (требуется JWT в Authorization: Bearer <token>)

- GET /notes — список заметок пользователя

- POST /notes — создание заметки

- GET /notes/{id} — получение заметки по ID

- PUT /notes/{id} — обновление заметки

- DELETE /notes/{id} — удаление заметки



