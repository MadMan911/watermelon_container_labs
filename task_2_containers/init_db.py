#!/usr/bin/env python3
import psycopg2
import time
import os
import sys

def init_database():
    """инициализация базы данных для jupyterhub"""
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
            print(f"попытка подключения к бд (попытка {attempt + 1}/{max_attempts})")
            conn = psycopg2.connect(**db_config)
            conn.autocommit = True
            cursor = conn.cursor()

            # создаем базу данных для jupyterhub, если не существует
            jupyterhub_db = os.getenv('JUPYTERHUB_DB', 'jupyterhub_db')
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{jupyterhub_db}'")
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {jupyterhub_db}")
                print(f"база данных {jupyterhub_db} создана")
            else:
                print(f"база данных {jupyterhub_db} уже существует")

            cursor.close()
            conn.close()
            print("инициализация базы данных завершена успешно")
            return True

        except psycopg2.OperationalError as e:
            print(f"ошибка подключения: {e}")
            attempt += 1
            time.sleep(2)
        except Exception as e:
            print(f"неожиданная ошибка: {e}")
            sys.exit(1)

    print("не удалось подключиться к базе данных после всех попыток")
    return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
