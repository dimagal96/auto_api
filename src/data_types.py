from datetime import datetime
from pydantic import BaseModel

class Car(BaseModel):
    model: str
    year: int
    color: str
    number: str
    type: int

class Accident(BaseModel):
    date: datetime
    location: str
    description: str

class AccidentCar(BaseModel):
    accident_id: int
    car_id: int

class Type(BaseModel):
    name: str