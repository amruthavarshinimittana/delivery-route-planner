# 🚚 Delivery Route Planner

A web application that optimizes delivery routes and calculates fuel and driver costs.

## What it does
- Enter delivery stops and distances from depot
- Automatically finds the most efficient order to visit stops
- Shows km saved and money saved vs unoptimized route
- Calculates fuel cost and driver cost
- Saves all routes to a database
- Shows charts and cost trends over time

## Tech Stack
- Python (OOP — 6 classes)
- Flask (web framework)
- SQLite (database)
- Pandas (data processing)
- Matplotlib (charts)

## How to Run
1. Install dependencies: `pip install flask pandas matplotlib`
2. Run: `python app.py`
3. Open browser: `http://127.0.0.1:5000`

## Project Structure
- `app.py` — Flask routes
- `models/stop.py` — Stop class
- `models/route.py` — Route class
- `models/route_optimizer.py` — Optimization algorithm
- `models/cost_calculator.py` — Cost calculations
- `models/route_db.py` — Database operations
- `models/report_generator.py` — Matplotlib charts
