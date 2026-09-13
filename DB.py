from sqlalchemy import create_engine


DATABASE_URL = "postgresql://postgres:postgres12345@localhost:5432/smartbus"

engine = create_engine(DATABASE_URL)

print("PostgreSQL connected successfully!")
