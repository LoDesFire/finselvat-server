# Finselvat Server

REST API для системы межведомственного обмена юридически значимыми документами.

## Описание проекта

Приложение эмулирует **Систему Б** в сценарии обмена документами между двумя информационными системами:

- **Система А** — инициирует запросы и отправляет документы
- **Система Б** — хранит документы и обеспечивает их целостность

### Формат данных

- **Конверт SignedApiData**: Все запросы и ответы оборачиваются в подписанный конверт (`Data`, `Sign`, `SignerCert`)
- **Кодировка**: JSON в UTF-8, бинарные данные в Base64
- **Время**: UTC в формате ISO 8601

## Установка и запуск

### Требования

- Python 3.13+
- Менеджер пакетов uv

### Локальная разработка

1. **Клонировать репозиторий**
   ```bash
   git clone <repository-url>
   cd finselvat-server
   ```

2. **Установить зависимости**
   ```bash
   uv sync
   ```

3. **Настроить окружение**
   ```bash
   cp .example.env .env
   ```

   Отредактируйте `.env` с вашими настройками:
   - `DB_PATH` — путь к SQLite базе данных (по умолчанию: `data/app.db`)
   - `DB_ECHO` — включение логирования SQL-запросов (по умолчанию: `True`)

4. **Выполнить миграции базы данных**
   ```bash
   alembic upgrade head
   ```

5. **Запустить сервер**
   ```bash
   uvicorn src.web.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Доступ к API**
   - API: http://localhost:8000

### Развёртывание в Docker

1. **Собрать образ**
   ```bash
   docker build -t finselvat-server .
   ```

2. **Запустить контейнер**
   ```bash
   docker run -d -p 8000:8000 --name finselvat-server finselvat-server
   ```

3. **С переменными окружения**
   ```bash
   docker run -d -p 8000:8000 \
     -e DB_PATH=sqlite:///app/data/app.db \
     -e DB_ECHO=false \
     --name finselvat-server \
     --volume "./data:/app/data:rw"
     finselvat-server
   ```

## Структура проекта

```
finselvat-server/
├── src/
│   ├── app/                    # Слой бизнес-логики
│   │   ├── transaction_repo.py # Репозиторий транзакций (доступ к данным)
│   │   └── transaction_service.py # Сервис транзакций (бизнес-логика)
│   ├── models/                 # SQLAlchemy ORM модели
│   │   ├── base.py            # Базовая конфигурация моделей
│   │   └── transaction.py     # Модель транзакции
│   ├── schemas/                # Pydantic схемы для валидации
│   │   ├── base_schema.py     # Базовая схема ответа
│   │   ├── error_schema.py    # Схема ошибки
│   │   ├── mixins.py          # Миксины схем
│   │   ├── search.py          # Схемы поисковых запросов
│   │   ├── signed_api_data.py # Схемы подписанных API данных
│   │   └── transactions.py    # Схемы транзакций
│   ├── utils/                  # Утилиты
│   │   ├── base64_utils.py    # Кодирование/декодирование Base64
│   │   ├── datetime_utils.py  # Утилиты даты/времени
│   │   └── hash_utils.py      # Утилиты верификации хэшей
│   ├── web/                    # Веб-слой (маршруты, обработчики)
│   │   ├── api/               # API эндпоинты
│   │   │   ├── healthcheck.py # Эндпоинт проверки здоровья
│   │   │   └── messages.py    # Эндпоинты сообщений
│   │   ├── dependencies/      # Зависимости FastAPI
│   │   │   ├── db_dependency.py    # Зависимость базы данных
│   │   │   ├── repo_dependencies.py # Зависимости репозиториев
│   │   │   └── service_dependencies.py # Зависимости сервисов
│   │   ├── main.py            # Инициализация FastAPI приложения
│   │   ├── routes.py          # Главный роутер
│   │   └── signed_api_route.py # Обработчик подписанных API маршрутов
│   ├── __init__.py
│   ├── constants.py           # Константы приложения
│   └── settings.py            # Настройки приложения (pydantic-settings)
├── alembic/                    # Миграции базы данных
│   ├── versions/              # Скрипты миграций
│   └── env.py                 # Конфигурация окружения Alembic
├── data/                       # Директория хранения базы данных
├── scripts/                    # Скрипты утилит
│   └── seed_data.py           # Скрипт наполнения базы тестовыми данными
├── alembic.ini                # Конфигурация Alembic
├── Dockerfile                 # Многоступенчатая сборка Docker
└── pyproject.toml             # Зависимости и метаданные проекта
```

## API эндпоинты

| Метод  | Эндпоинт                 | Описание                                                        |
|--------|--------------------------|-----------------------------------------------------------------|
| GET    | `/api/health`            | Проверка доступности сервиса                                    |
| POST   | `/api/messages/incoming` | Отправка сообщений от Системы А в Систему Б. Возвращает квитки  |
| POST   | `/api/messages/outgoing` | Получение входящих сообщений для Системы А за указанный период  |

Все запросы и ответы используют **конверт SignedApiData** с полями: `Data` (Base64), `Sign` (Base64), `SignerCert` (Base64).

## Примеры запросов

См. [EXAMPLES.md](EXAMPLES.md) с примерами curl-запросов для всех эндпоинтов.

## Технологии

- **FastAPI** — современный асинхронный веб-фреймворк
- **SQLAlchemy** — SQL-инструментарий и ORM
- **Pydantic** — валидация данных
- **Alembic** — миграции базы данных
- **uvicorn** — ASGI-сервер
