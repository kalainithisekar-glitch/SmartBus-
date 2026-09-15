from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="smartbus",
        user="postgres",
        password="postgres12345",
        port="5432"
    )


class User(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str = "PASSENGER"


@app.post("/users")
def create_user(user: User):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (name, email, phone, password, role)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            user.name,
            user.email,
            user.phone,
            user.password,
            user.role
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "User added successfully!"}

    cursor.close()
    connection.close()

    return users
