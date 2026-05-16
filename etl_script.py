from sqlalchemy import create_engine, text
from datetime import date


MAIN_DB_URL = "postgresql://postgres:admin123@localhost:5432/main_db"
REPORTING_DB_URL = "postgresql://postgres:admin123@localhost:5432/reporting_db"

engine_main = create_engine(MAIN_DB_URL)
engine_reporting = create_engine(REPORTING_DB_URL)

def run_etl():
    print("Magsugod na ang ETL process...")
    
    
    today = date.today()
    
    
    query_extract = """
        SELECT 
            COALESCE(SUM(total_price), 0) as total_revenue,
            COUNT(id) as total_orders
        FROM orders
        WHERE DATE(created_at) = CURRENT_DATE;
    """
    
    with engine_main.connect() as conn_main:
        result = conn_main.execute(text(query_extract)).mappings().first()
        total_revenue = result['total_revenue']
        total_orders = result['total_orders']
        
    print(f"Data Extracted: Revenue = P{total_revenue}, Orders = {total_orders}")

    

    query_load = """
        INSERT INTO daily_sales_summary (report_date, total_revenue, total_orders)
        VALUES (:report_date, :total_revenue, :total_orders)
        ON CONFLICT (report_date) 
        DO UPDATE SET 
            total_revenue = EXCLUDED.total_revenue,
            total_orders = EXCLUDED.total_orders;
    """
    
    with engine_reporting.connect() as conn_reporting:
        conn_reporting.execute(
            text(query_load), 
            {
                "report_date": today, 
                "total_revenue": total_revenue, 
                "total_orders": total_orders
            }
        )

        conn_reporting.commit()
        
    print("ETL Process Successful! Na-transfer na ang data sa reporting_db.")

if __name__ == "__main__":
    run_etl()