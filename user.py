from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is working!"}


@app.get("/database")
def db_connection():

    try:
        connection = psycopg2.connect(
            host="localhost",
            database="smartbus",
            user="postgres",
            password="postgres12345",
            port="5432"
        )

        connection.close()

        return {"message": "PostgreSQL connected successfully!"}

    except Exception as e:
        return {"error": str(e)}
