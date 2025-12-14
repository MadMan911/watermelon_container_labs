#!/usr/bin/env python3
import psycopg2
import time
import os

def init_database():
    """Инициализация базы данных для JupyterHub"""
    db_config = {
        'host': os.getenv('POSTGRES_HOST', 'postgres'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'database': os.getenv('POSTGRES_DB', 'postgres')
    }

    max_attempts = 30
    attempt = 0

    while attempt < max_attempts:
        try:
            print(f"Попытка подключения к БД (попытка {attempt + 1}/{max_attempts})")
            conn = psycopg2.connect(**db_config)
            conn.autocommit = True
            cursor = conn.cursor()

            # Создаем базу данных для JupyterHub, если не существует
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'jupyterhub_db'")
            if not cursor.fetchone():
                cursor.execute("CREATE DATABASE jupyterhub_db")
                print("База данных jupyterhub_db создана")
            else:
                print("База данных jupyterhub_db уже существует")

            cursor.close()
            conn.close()
            print("Инициализация базы данных завершена успешно")
            return True

        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения: {e}")
            attempt += 1
            time.sleep(2)

    print("Не удалось подключиться к базе данных после всех попыток")
    return False

if __name__ == "__main__":
    init_database()
