import sqlite3
import json
from datetime import datetime

DB_PATH = "routes.db"

class RouteDB:
    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                stops TEXT NOT NULL,
                total_distance REAL NOT NULL,
                estimated_time REAL NOT NULL,
                fuel_cost REAL NOT NULL,
                driver_cost REAL NOT NULL,
                total_cost REAL NOT NULL,
                fuel_price REAL NOT NULL,
                mileage REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_route(self, route_data):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO routes 
            (date, stops, total_distance, estimated_time, fuel_cost, driver_cost, total_cost, fuel_price, mileage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            json.dumps(route_data["stops"]),
            route_data["total_distance"],
            route_data["estimated_time"],
            route_data["fuel_cost"],
            route_data["driver_cost"],
            route_data["total_cost"],
            route_data["fuel_price"],
            route_data["mileage"]
        ))
        conn.commit()
        conn.close()

    def get_all_routes(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routes ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "date": row[1],
                "stops": json.loads(row[2]),
                "total_distance": row[3],
                "estimated_time": row[4],
                "fuel_cost": row[5],
                "driver_cost": row[6],
                "total_cost": row[7],
                "fuel_price": row[8],
                "mileage": row[9]
            })
        return results

    def get_recent_routes(self, limit=10):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routes ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "date": row[1],
                "stops": json.loads(row[2]),
                "total_distance": row[3],
                "estimated_time": row[4],
                "fuel_cost": row[5],
                "driver_cost": row[6],
                "total_cost": row[7]
            })
        return results

    def delete_route(self, route_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM routes WHERE id = ?", (route_id,))
        conn.commit()
        conn.close()