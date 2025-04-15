from datetime import datetime
from pydantic import BaseModel

class Car(BaseModel):
    model: str
    year: int
    color: str
    number: str
    type: int

class CarUpdate(BaseModel):
    id: int
    model: str = None
    year: int = None
    color: str = None
    number: str = None
    type: int = None

class Accident(BaseModel):
    date: datetime
    location: str
    description: str

class AccidentUpdate(BaseModel):
    id: int
    date: datetime = None
    location: str = None
    description: str = None

class AccidentCar(BaseModel):
    accident_id: int
    car_id: int

class Type(BaseModel):
    name: str