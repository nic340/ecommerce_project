import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

DATABASE_URL = os.getenv("MAIN_DB_URL", "postgresql://postgres:admin123@localhost:5432/main_db")
engine = create_engine(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "Ang imong Backend buhi na!"}

@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM products"))
            products = [dict(row) for row in result.mappings()]
            return {"status": "Connected!", "data": products}
    except Exception as e:
        return {"status": "Error", "message": str(e)}