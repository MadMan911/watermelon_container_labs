# Лабораторная работа №2: Docker Compose

## Описание проекта

Проект представляет собой многосервисное приложение на основе Docker Compose, включающее:

1. **init** - сервис инициализации базы данных (одноразовый контейнер)
2. **jupyterhub** - основное веб-приложение для запуска Jupyter notebooks
3. **postgres** - база данных PostgreSQL для хранения данных JupyterHub

## Архитектура

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Jupyter   │    │   Init      │    │ PostgreSQL  │
│   Hub App   │◄───┤   Service   │◄───┤ Database    │
│  (Port 8000)│    │ (One-time)  │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Сервисы

### Init Service
- **Образ**: python:3.9-slim
- **Назначение**: Инициализация базы данных для JupyterHub
- **Особенности**:
  - Одноразовый контейнер (profiles: init)
  - Ждет готовности PostgreSQL
  - Создает базу данных jupyterhub_db при необходимости

### JupyterHub Service
- **Образ**: Собственный (jupyterhub-custom:latest), собирается из Dockerfile
- **Порт**: 8000 (прокидывается наружу)
- **Особенности**:
  - Автоматическая сборка образа
  - Подключенные volumes для конфигурации и данных
  - Healthcheck для проверки работоспособности
  - Depends on init и postgres сервисы

### PostgreSQL Service
- **Образ**: postgres:14
- **Особенности**:
  - Volume для персистентности данных
  - Healthcheck для проверки подключения к БД

## Запуск

```bash
# Запуск всех сервисов
docker-compose up -d

# Запуск только инициализации и JupyterHub (без БД)
docker-compose --profile init up jupyterhub

# Остановка
docker-compose down

# Остановка с удалением volumes
docker-compose down -v
```

## Переменные окружения (.env)

Все переменные определены в файле `.env`:
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` - настройки PostgreSQL
- `JUPYTER_PORT` - порт для JupyterHub
- `JUPYTERHUB_DB` - имя базы данных для JupyterHub

## Сеть

Все сервисы подключены к общей сети `jupyter_network` (тип bridge).

## Volumes

- `postgres_data` - данные PostgreSQL
- `jupyterhub_data` - данные пользователей JupyterHub

## Ответы на вопросы

### 1. Можно ли ограничивать ресурсы (например, память или CPU) для сервисов в docker-compose.yml?

Да, можно ограничивать ресурсы для сервисов в docker-compose.yml. Для этого используются параметры `deploy.resources`:

```yaml
services:
  service_name:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

- `limits` - максимальные значения ресурсов
- `reservations` - гарантированные минимальные значения

### 2. Как можно запустить только определенный сервис из docker-compose.yml, не запуская остальные?

Для запуска только определенного сервиса используется команда:

```bash
docker-compose up <service_name>
```

Например:
```bash
docker-compose up jupyterhub  # запустит только jupyterhub и его зависимости
```

Если нужно запустить сервис без зависимостей:
```bash
docker-compose up --no-deps <service_name>
```

Для одноразовых сервисов (как init в данном проекте) можно использовать profiles:
```bash
docker-compose --profile init up <service_name>
```
