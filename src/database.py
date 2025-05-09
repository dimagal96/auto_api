import psycopg2
from psycopg2 import sql
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
        query = "SELECT model, year, color, number, type FROM cars WHERE id = %s"

        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()

        if row:
            return Car(model=row[0], year=row[1], color=row[2], number=row[3], type=row[4])

        return None

    def update_car(self, car: CarUpdate):
        fields = {k: v for k, v in car.model_dump().items() if k != "id" and v is not None}
        if not fields:
            return False

        query = sql.SQL("UPDATE cars SET {updates} WHERE id = %(id)s").format(
            updates=sql.SQL(", ").join(
                sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder(k)]) for k in fields
            )
        )
        params = {**fields, "id": car.id}

        self.cursor.execute(query, params)
        self.connection.commit()
        return None

    def delete_car(self, id: int):
        query = "DELETE FROM cars WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.connection.commit()
        return None

    def get_cars(self):
        query = "SELECT * FROM cars"

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        cars = []

        for elem in results:
            cars.append({
                "id": elem[0],
                "data": Car(model=elem[1], year=elem[2], color=elem[3], number=elem[4], type=elem[5])
            })

        return cars

    def get_accidents(self):
        query = "SELECT * FROM accidents"

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        accidents = []

        for elem in results:
            accidents.append({
                "id": elem[0],
                "data": Accident(date=elem[1], location=elem[2], description=elem[3])
            })

        return accidents

    def get_accident(self, id: int):
        query = "SELECT date, location, description FROM accidents WHERE id = %s"

        self.cursor.execute(query, (id,))
        row_accident_data = self.cursor.fetchone()

        query = "SELECT car_id FROM accidents_cars WHERE accident_id = %s"

        self.cursor.execute(query, (id,))
        row_accident_cars_data = self.cursor.fetchone()

        if not row_accident_data:
            return None

        return {
            "accident": Accident(date=row_accident_data[0], location=row_accident_data[1], description=row_accident_data[2]),
            "cars": row_accident_cars_data
        }

    def save_accident(self, accident: Accident):
        query = """
            INSERT INTO accidents (date, location, description)
            VALUES (%s, %s, %s)
            RETURNING id
        """

        self.cursor.execute(query, (accident.date, accident.location, accident.description))
        accident_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return accident_id

    def update_accident(self, accident: AccidentUpdate):
        fields = {k: v for k, v in accident.model_dump().items() if k != "id" and v is not None}
        if not fields:
            return False

        query = sql.SQL("UPDATE accidents SET {updates} WHERE id = %(id)s").format(
            updates=sql.SQL(", ").join(
                sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder(k)]) for k in fields
            )
        )
        params = {**fields, "id": accident.id}

        self.cursor.execute(query, params)
        self.connection.commit()
        return None

    def delete_accident(self, id: int):
        query = "DELETE FROM accidents WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.connection.commit()
        return None

    def get_car_accidents(self, id: int):
        query = """
            SELECT accidents.*
            FROM accidents
            JOIN accidents_cars ON accidents.id = accidents_cars.accident_id
            WHERE accidents_cars.car_id = %s
        """

        self.cursor.execute(query, (id,))
        results = self.cursor.fetchall()
        accidents = {}

        for elem in results:
            accidents[elem[0]] = Accident(date=elem[1], location=elem[2], description=elem[3])

        return accidents

    def save_accident_car(self, accident_car: AccidentCar):
        query = """
            INSERT INTO accidents_cars (accident_id, car_id)
            VALUES (%s, %s)
            RETURNING id
        """

        self.cursor.execute(query, (accident_car.accident_id, accident_car.car_id))
        accident_car_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return accident_car_id

    def delete_accident_car(self, id: int):
        query = "DELETE FROM accidents_cars WHERE accident_id = %s"
        self.cursor.execute(query, (id,))
        self.connection.commit()
        return None

    def get_types(self):
        query = "SELECT * FROM types"

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        types = []

        for elem in results:
            types.append({
                "id": elem[0],
                "data": Type(name=elem[1])
            })

        return types

    def save_type(self, type: Type):
        query = """
            INSERT INTO types (name)
            VALUES (%s)
            RETURNING id
        """

        self.cursor.execute(query, (type.name,))
        type_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return type_id
