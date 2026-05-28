import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAIN_DB_URL = os.getenv("MAIN_DB_URL", "postgresql://postgres:admin123@localhost:5432/main_db")
REPORTING_DB_URL = os.getenv("REPORTING_DB_URL", "postgresql://postgres:admin123@localhost:5432/reporting_db")

engine_main = create_engine(MAIN_DB_URL)
engine_reporting = create_engine(REPORTING_DB_URL)

@app.get("/")
def read_root():
    return {"message": "Ang imong Backend buhi na!"}

@app.get("/test-db")
def test_db():
    try:
        with engine_main.connect() as connection:
            result = connection.execute(text("SELECT * FROM products"))
            products = [dict(row) for row in result.mappings()]
            return {"status": "Connected!", "data": products}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

@app.get("/reporting-db")
def get_reporting_data():
    try:
        with engine_reporting.connect() as connection:
            result = connection.execute(text("SELECT * FROM daily_sales_summary ORDER BY report_date DESC"))
            summary = [dict(row) for row in result.mappings()]
            return {"status": "Connected!", "data": summary}
    except Exception as e:
        return {"status": "Error", "message": str(e)}