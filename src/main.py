import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from database import Database
from data_types import *

load_dotenv()

app = FastAPI()
database = Database(
    database="postgres",
    user="postgres",
    password=os.getenv('DATABASE_PASSWORD'),
    host="localhost",
    port=5432,
    options="-c search_path={}".format(os.getenv('DATABASE_SCHEMA'))
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

@app.put('/car')
async def save_car(car: Car):
    return database.save_car(car)

@app.delete('/car')
async def delete_car(id: int):
    return database.delete_car(id)

@app.get('/accident')
async def get_accident(id: int):
    return {
        "id": id,
        "data": database.get_accident(id)
    }

@app.put('/accident')
async def save_accident(accident: Accident):
    return database.save_accident(accident)

@app.delete('/accident')
async def delete_accident(id: int):
    return database.delete_accident(id)

@app.get('/car/accidents')
async def get_car_accidents(id: int):
    return {
        "id": id,
        "data": database.get_car_accidents(id)
    }

@app.put('/car/accidents')
async def save_car_accident(accident_car: AccidentCar):
    return database.save_accident_car(accident_car)

@app.delete('/car/accidents')
async def delete_car_accident(id: int):
    return database.delete_accident_car(id)

@app.get('/types')
async def get_types():
    return database.get_types()
