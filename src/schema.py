import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_SCHEMA = os.getenv("DATABASE_SCHEMA")

with psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
) as conn:
    with conn.cursor() as cur:
        cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
            sql.Identifier(DB_SCHEMA)
        ))

    conn.commit()

with psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    options=f"-c search_path={DB_SCHEMA}"
) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS types (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                id SERIAL PRIMARY KEY,
                model TEXT NOT NULL,
                year INTEGER CHECK (year > 1885),
                color TEXT NOT NULL,
                number VARCHAR(16) UNIQUE,
                type INTEGER NOT NULL REFERENCES types(id) ON DELETE CASCADE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS accidents (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS accidents_cars (
                id SERIAL PRIMARY KEY,
                accident_id INTEGER NOT NULL REFERENCES accidents(id) ON DELETE CASCADE,
                car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE
            );
        """)

    conn.commit()
