import psycopg2
from data_types import *

class Database:
    def __init__(self, **connargs):
        self.connection = psycopg2.connect(**connargs)
        self.cursor = self.connection.cursor()

    def save_car(self, car: Car) -> int:
        query = """
            INSERT INTO cars (model, year, color, number, type)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """

        self.cursor.execute(query, (car.model, car.year, car.color, car.number, car.type))
        car_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return car_id

    def get_car(self, id: int) -> Car | None:
        query = """
            SELECT model, year, color, number, type FROM cars WHERE id = %s
        """

        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()

        if row:
            return Car(model=row[0], year=row[1], color=row[2], number=row[3], type=row[4])

        return None
