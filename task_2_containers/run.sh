#!/bin/bash

# Скрипт запуска Docker Compose для лабораторной работы №2

set -e

echo "=== Лабораторная работа №2: Docker Compose ==="
echo "Запуск многосервисного приложения JupyterHub + PostgreSQL"
echo

# Проверка наличия docker и docker-compose
if ! command -v docker &> /dev/null; then
    echo "Ошибка: Docker не установлен или не доступен"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Ошибка: Docker Compose не установлен или не доступен"
    exit 1
fi

echo "Проверка наличия файлов конфигурации..."
if [ ! -f ".env" ]; then
    echo "Ошибка: файл .env не найден"
    exit 1
fi

if [ ! -f "docker-compose.yml" ]; then
    echo "Ошибка: файл docker-compose.yml не найден"
    exit 1
fi

echo "OK"
echo

# Опции запуска
case "${1:-all}" in
    "init")
        echo "Запуск только инициализации базы данных..."
        docker-compose --profile init up init
        ;;
    "jupyterhub")
        echo "Запуск только JupyterHub..."
        docker-compose up --no-deps jupyterhub
        ;;
    "postgres")
        echo "Запуск только PostgreSQL..."
        docker-compose up --no-deps postgres
        ;;
    "all"|*)
        echo "Запуск всех сервисов..."
        echo "Это может занять некоторое время при первом запуске"
        echo "JupyterHub будет доступен на http://localhost:8000"
        echo
        docker-compose up -d
        echo
        echo "Сервисы запущены!"
        echo "Для просмотра логов: docker-compose logs -f"
        echo "Для остановки: docker-compose down"
        ;;
esac
