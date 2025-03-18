import os
from dotenv import load_dotenv
from fastapi import FastAPI
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
async def get_car(id: int):
    return {
        "id": id,
        "data": database.get_car(id)
    }

@app.put('/cars')
async def save_car(car: Car):
    return database.save_car(car)