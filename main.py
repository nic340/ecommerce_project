import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BuyRequest(BaseModel):
    product_id: int
    quantity: int

class LoginRequest(BaseModel):
    username: str
    password: str

MAIN_DB_URL = os.getenv("MAIN_DB_URL", "postgresql://postgres:admin123@localhost:5432/main_db")
REPORTING_DB_URL = os.getenv("REPORTING_DB_URL", "postgresql://postgres:admin123@localhost:5432/reporting_db")

engine_main = create_engine(MAIN_DB_URL)
engine_reporting = create_engine(REPORTING_DB_URL)

@app.get("/")
def read_root():
    return {"message": "Cloud Core Engine Status Online"}

@app.post("/api/login")
def login(req: LoginRequest):
    if req.username == "admin" and req.password == "admin123":
        return {"status": "Authenticated", "token": "session-token-secure-99"}
    raise HTTPException(status_code=401, detail="Invalid administrator credentials")

@app.get("/test-db")
def test_db():
    try:
        with engine_main.connect() as connection:
            result = connection.execute(text("SELECT * FROM products ORDER BY id ASC"))
            products = [dict(row) for row in result.mappings()]
            return {"status": "Connected!", "data": products}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

@app.post("/buy")
def buy_product(req: BuyRequest):
    try:
        with engine_main.connect() as connection:
            product = connection.execute(
                text("SELECT * FROM products WHERE id = :id"), 
                {"id": req.product_id}
            ).mappings().first()
            
            if not product:
                return {"status": "Error", "message": "Product records database empty"}
            
            if product["stock"] < req.quantity:
                return {"status": "Error", "message": "Insufficient retail inventory"}
            
            total_price = float(product["price"]) * req.quantity
            new_stock = product["stock"] - req.quantity
            
            connection.execute(
                text("UPDATE products SET stock = :stock WHERE id = :id"),
                {"stock": new_stock, "id": req.product_id}
            )
            
            connection.execute(
                text("INSERT INTO orders (product_id, quantity, total_price) VALUES (:p_id, :qty, :total)"),
                {"p_id": req.product_id, "qty": req.quantity, "total": total_price}
            )
            
            connection.commit()
            return {"status": "Success", "message": "Transaction commit verified"}
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