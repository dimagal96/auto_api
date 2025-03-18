import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    database="postgres",
    user="postgres",
    password=os.getenv('DATABASE_PASSWORD'),
    host="localhost",
    port=5432,
    options="-c search_path={}".format(os.getenv('DATABASE_SCHEMA'))
)

cursor = connection.cursor()

cursor.execute('CREATE TABLE types (id SERIAL PRIMARY KEY, ' +
               'name TEXT NOT NULL)')
cursor.execute('CREATE TABLE cars (id SERIAL PRIMARY KEY, ' +
               'model TEXT NOT NULL, ' +
               'year INTEGER CHECK (year > 1885), ' +
               'color TEXT NOT NULL, ' +
               'number VARCHAR(16) UNIQUE, ' +
               'type INTEGER NOT NULL REFERENCES types(id) ON DELETE CASCADE)')
cursor.execute('CREATE TABLE accidents (id SERIAL PRIMARY KEY, ' +
               'date TIMESTAMP NOT NULL, ' +
               'location TEXT NOT NULL, ' +
               'description TEXT NOT NULL)')
cursor.execute('CREATE TABLE accidents_cars (id SERIAL PRIMARY KEY, ' +
               'accident_id INTEGER NOT NULL REFERENCES accidents(id) ON DELETE CASCADE, ' +
               'car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE)')
connection.commit()

cursor.close()
connection.close()
