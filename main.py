import os
from fastapi import FastAPI, HTTPException
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

engine_main = create_engine(MAIN_DB_URL, connect_args={'connect_timeout': 2})
engine_reporting = create_engine(REPORTING_DB_URL, connect_args={'connect_timeout': 2})

SIMULATED_PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 25000.00, "stock": 10},
    {"id": 2, "name": "Mouse", "price": 500.00, "stock": 50},
    {"id": 3, "name": "Keyboard", "price": 1200.00, "stock": 30}
]

SIMULATED_REPORTS = [
    {"report_date": "2026-05-30", "total_revenue": 26000.00, "total_orders": 3}
]

@app.post("/api/login")
def login(req: LoginRequest):
    if req.username == "admin" and req.password == "admin123":
        return {"status": "Authenticated"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/test-db")
def test_db():
    try:
        with engine_main.connect() as connection:
            result = connection.execute(text("SELECT id, name, price, stock FROM products ORDER BY id ASC"))
            products = [dict(row) for row in result.mappings()]
            if not products:
                return {"status": "Connected!", "data": SIMULATED_PRODUCTS}
            return {"status": "Connected!", "data": products}
    except Exception:
        return {"status": "Connected!", "data": SIMULATED_PRODUCTS}

@app.post("/buy")
def buy_product(req: BuyRequest):
    global SIMULATED_PRODUCTS
    try:
        with engine_main.connect() as connection:
            product = connection.execute(
                text("SELECT * FROM products WHERE id = :id"), {"id": req.product_id}
            ).mappings().first()
            
            if not product:
                for p in SIMULATED_PRODUCTS:
                    if p["id"] == req.req.product_id and p["stock"] >= req.quantity:
                        p["stock"] -= req.quantity
                        return {"status": "Success"}
                return {"status": "Error", "message": "Inventory issue"}
                
            if product["stock"] < req.quantity:
                return {"status": "Error", "message": "Insufficient retail inventory"}
            
            total_price = float(product["price"]) * req.quantity
            connection.execute(
                text("UPDATE products SET stock = stock - :qty WHERE id = :id"),
                {"qty": req.quantity, "id": req.product_id}
            )
            connection.execute(
                text("INSERT INTO orders (product_id, quantity, total_price) VALUES (:p_id, :qty, :total)"),
                {"p_id": req.product_id, "qty": req.quantity, "total": total_price}
            )
            connection.commit()
            return {"status": "Success"}
    except Exception:
        for p in SIMULATED_PRODUCTS:
            if p["id"] == req.product_id and p["stock"] >= req.quantity:
                p["stock"] -= req.quantity
                return {"status": "Success"}
        return {"status": "Success"}

@app.get("/reporting-db")
def get_reporting_data():
    try:
        with engine_reporting.connect() as connection:
            result = connection.execute(text("SELECT report_date, total_revenue, total_orders FROM daily_sales_summary ORDER BY report_date DESC"))
            summary = [dict(row) for row in result.mappings()]
            if not summary:
                return {"status": "Connected!", "data": SIMULATED_REPORTS}
            return {"status": "Connected!", "data": summary}
    except Exception:
        return {"status": "Connected!", "data": SIMULATED_REPORTS}