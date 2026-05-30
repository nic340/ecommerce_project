# Archive Shop Storefront & Analytics: Cloud Computing Final Project

Archive Shop is a demo-ready, full-stack enterprise e-commerce hardware platform specializing in essential computer hardware components. Deployed entirely on a **Hostinger Cloud VPS**, this project highlights a single-origin deployment combining a modular FastAPI asset routine, a PostgreSQL transactional layer (`main_db`), an isolated analytical processing layer (`reporting_db`), and a Python-driven Batch ETL pipeline.

## Live Deployment

You can access the deployed project here:

**Live Site:** [http://187.127.118.153:8000/](http://187.127.118.153:8000/)

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | Unified Single-Origin HTML5, Core JavaScript Router, Tailwind CSS via CDN |
| Backend | FastAPI Framework, Uvicorn ASGI Server Application Process |
| Main DB | PostgreSQL Database Instance (`main_db` for OLTP transactional data) |
| Reporting DB | PostgreSQL Database Instance (`reporting_db` for OLAP data analytics) |
| ETL | Modular Python Batch Engine script running manually or via server scheduling |
| VPS Runtime | Ubuntu OS Environment, Linux Terminal Framework, Virtual Environments (`venv`) |

---

## Features

- Modern responsive enterprise interface tailored for IT computer components.
- Live header display featuring dynamic metadata tracking ("Cloud Computing Final Project").
- Dynamic card inventory displaying computer entities: Laptops (💻), Mice (🖱️), and Keyboards (⌨️).
- Real-time stock level metric track limits configured into a live stock tracking indicator.
- Single-Origin hosting layout running the frontend over the same production endpoint host.
- Asynchronous, direct-action purchase triggers linked directly to transactional endpoints.
- Independent database schema mapping to prevent client transactions from affecting analytics reporting.
- Controlled Batch ETL execution loops designed to safely extract database rows.

---

## Architecture

```mermaid
flowchart LR
    Browser["Client Browser Layout"] -->|Port 8000 Static File Routing| FastAPI["FastAPI Core Engine"]
    FastAPI -->|Fetch / Buy Endpoints| MainDB["PostgreSQL main_db (OLTP)"]
    ETL["etl_script.py Process Execution"] -->|Extract Stage| MainDB
    ETL -->|Load Stage Summary Data| ReportingDB["PostgreSQL reporting_db (OLAP)"]
    FastAPI -->|Analytics Ingestion| ReportingDB
Database SchemaTransactional Database (main_db)products: id (PK), name, price, stockorders: id (PK), product_id, quantity_ordered, timestampAnalytical Database (reporting_db)dim_products_summaryfact_sales_aggregatestotal_revenue_indexAPI EndpointsMethodEndpointPurposeScopeGET/Serves the decoupled storefront asset context file (index.html)Frontend DeliveryGET/productsPulls core product catalog matrix and stock states from databaseCatalog DataPOST/buy/{id}Processes inventory transactions, managing core schema metricsTransaction EngineEnvironment VariablesProject configuration variables file structure (~/ecommerce_project/.env):Code snippetDATABASE_URL=postgresql://postgres:yoursecurepassword@localhost:5432/main_db
REPORTING_DATABASE_URL=postgresql://postgres:yoursecurepassword@localhost:5432/reporting_db
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ETL ProcessRun the batch engine execution task manually using your terminal prompt:Bashcd ~/ecommerce_project
source venv/bin/activate
python3 etl_script.py
The ETL processes un-synced inventory lines inside main_db, builds total transaction calculations, manages sales computations, and updates row segments inside reporting_db.Demo FlowOpen the remote cloud deployment link in your desktop browser: http://187.127.118.153:8000/.Inspect the operational stock counter variables displayed inside the product item views.Click the "BUY NOW" command on any inventory card (e.g., Mouse) to execute an active transaction log.Verify the database stock change from the UI state (e.g., Inventory drops from 50 down to 49 items).Open your secondary terminal console panel and execute the automated process loop: python3 etl_script.py.Inspect the live data logs printed on screen confirming successful batch tracking updates.Refresh the separate Analytical views to view calculated sales parameters (₱) updated by the pipeline logic.Verification CommandsExecute these verification tasks inside the virtual terminal workspace to confirm system compliance:Bashpwd

python3 -m compileall main.py etl_script.py

fuser -k 8000/tcp

python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Troubleshooting MatrixBlank Storefront Dashboard Cards: Ensure you are accessing the server domain over its explicit network port assignment (:8000). Clear local browser caches by executing a target hard reload loop via Ctrl + F5.Process Binding Collisions (Address already in use): Execute an immediate system process cleanup task using fuser -k 8000/tcp to release active listeners before deploying new instances.Stagnant Graph Analytics Parameters: Ensure you run the programmatic batch synchronization routine (python3 etl_script.py) in your terminal window after checkout actions to update the analytical schema.
