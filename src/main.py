import os
from dotenv import load_dotenv
from fastapi import FastAPI, Body, Path
from database import Database
from data_types import *

load_dotenv()

DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_SCHEMA = os.getenv("DATABASE_SCHEMA")

app = FastAPI()
database = Database(
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    options=f"-c search_path={DB_SCHEMA}"
)

@app.get('/cars')
async def get_cars():
    return database.get_cars()

@app.get('/accidents')
async def get_accidents():
    return database.get_accidents()

@app.get('/car')
async def get_car(id: int):
    return {
        "id": id,
        "data": database.get_car(id)
    }

@app.post('/car')
async def save_car(car: Car):
    return database.save_car(car)

@app.put('/car')
async def put_car(car: CarUpdate = Body(...)):
    return database.update_car(car)

@app.delete('/car')
async def delete_car(id: int):
    return database.delete_car(id)

@app.get('/accident')
async def get_accident(id: int):
    return {
        "id": id,
        "data": database.get_accident(id)
    }

@app.post('/accident')
async def save_accident(accident: Accident):
    return database.save_accident(accident)

@app.put('/accident')
async def put_accident(accident: AccidentUpdate = Body(...)):
    return database.update_accident(accident)

@app.delete('/accident')
async def delete_accident(id: int):
    return database.delete_accident(id)

@app.get('/car/accidents')
async def get_car_accidents(id: int):
    return {
        "id": id,
        "data": database.get_car_accidents(id)
    }

@app.post('/car/accidents')
async def save_car_accident(accident_car: AccidentCar):
    return database.save_accident_car(accident_car)

@app.delete('/car/accidents')
async def delete_car_accident(id: int):
    return database.delete_accident_car(id)

@app.get('/types')
async def get_types():
    return database.get_types()

@app.post('/types')
async def save_type(type: Type):
    return database.save_type(type)
