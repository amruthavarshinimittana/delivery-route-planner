from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import io
from models.stop import Stop
from models.route_optimizer import RouteOptimizer
from models.cost_calculator import CostCalculator
from models.route_db import RouteDB
from models.report_generator import ReportGenerator

app = Flask(__name__)
app.secret_key = "delivery_secret_123"

db = RouteDB()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    charts = {}

    if request.method == "POST":
        fuel_price  = float(request.form.get("fuel_price", 100))
        mileage     = float(request.form.get("mileage", 12))
        driver_rate = float(request.form.get("driver_rate", 50))

        names     = request.form.getlist("stop_name[]")
        distances = request.form.getlist("stop_distance[]")

        stops = []
        for i, (name, dist) in enumerate(zip(names, distances)):
            name = name.strip()
            dist = dist.strip()
            if name and dist:
                try:
                    stops.append(Stop(i+1, name, float(dist)))
                except ValueError:
                    flash(f"Invalid distance for '{name}'.", "error")
                    return redirect(url_for("index"))

        if len(stops) < 2:
            flash("Please add at least 2 stops.", "error")
            return redirect(url_for("index"))

        optimizer    = RouteOptimizer(stops)
        unopt_dist   = optimizer.unoptimized_distance()
        route        = optimizer.optimize(fuel_price, mileage)

        calc         = CostCalculator(fuel_price, mileage, driver_rate)
        breakdown    = calc.cost_breakdown(route.total_distance(), route.estimated_time_hours())
        unopt_cost   = calc.total_cost(unopt_dist, round(unopt_dist/40, 2))
        savings_km   = round(unopt_dist - route.total_distance(), 2)
        savings_cost = round(unopt_cost - breakdown["total_cost"], 2)

        rg = ReportGenerator([])
        charts["route_stops"] = rg.route_stop_chart(
            route.stop_names(),
            [s.distance_from_depot for s in route.stops]
        )
        charts["cost_pie"] = rg.cost_breakdown_chart(
            breakdown["fuel_cost"], breakdown["driver_cost"]
        )

        result = {
            "stops": route.stop_names(),
            "total_distance": route.total_distance(),
            "unopt_distance": unopt_dist,
            "savings_km": savings_km,
            "savings_cost": savings_cost,
            "estimated_time": route.estimated_time_hours(),
            "fuel_cost": breakdown["fuel_cost"],
            "driver_cost": breakdown["driver_cost"],
            "total_cost": breakdown["total_cost"],
            "litres_used": breakdown["litres_used"],
            "fuel_price": fuel_price,
            "mileage": mileage
        }

        db.save_route(result)
        flash("Route optimized and saved!", "success")

    return render_template("index.html", result=result, charts=charts)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    result = None
    charts = {}

    if request.method == "POST":
        file        = request.files.get("csv_file")
        fuel_price  = float(request.form.get("fuel_price", 100))
        mileage     = float(request.form.get("mileage", 12))
        driver_rate = float(request.form.get("driver_rate", 50))

        if not file or file.filename == "":
            flash("Please upload a CSV file.", "error")
            return redirect(url_for("upload"))

        try:
            stream = io.StringIO(file.stream.read().decode("utf-8"))
            df = pd.read_csv(stream)
            df.columns = df.columns.str.strip().str.lower()

            if "stop_name" not in df.columns or "distance_km" not in df.columns:
                flash("CSV must have columns: stop_name, distance_km", "error")
                return redirect(url_for("upload"))

            stops = []
            for i, row in df.iterrows():
                stops.append(Stop(i+1, str(row["stop_name"]).strip(),
                                  float(row["distance_km"])))

            optimizer    = RouteOptimizer(stops)
            unopt_dist   = optimizer.unoptimized_distance()
            route        = optimizer.optimize(fuel_price, mileage)

            calc         = CostCalculator(fuel_price, mileage, driver_rate)
            breakdown    = calc.cost_breakdown(route.total_distance(), route.estimated_time_hours())
            unopt_cost   = calc.total_cost(unopt_dist, round(unopt_dist/40, 2))
            savings_km   = round(unopt_dist - route.total_distance(), 2)
            savings_cost = round(unopt_cost - breakdown["total_cost"], 2)

            rg = ReportGenerator([])
            charts["route_stops"] = rg.route_stop_chart(
                route.stop_names(),
                [s.distance_from_depot for s in route.stops]
            )
            charts["cost_pie"] = rg.cost_breakdown_chart(
                breakdown["fuel_cost"], breakdown["driver_cost"]
            )

            result = {
                "stops": route.stop_names(),
                "total_distance": route.total_distance(),
                "unopt_distance": unopt_dist,
                "savings_km": savings_km,
                "savings_cost": savings_cost,
                "estimated_time": route.estimated_time_hours(),
                "fuel_cost": breakdown["fuel_cost"],
                "driver_cost": breakdown["driver_cost"],
                "total_cost": breakdown["total_cost"],
                "litres_used": breakdown["litres_used"],
                "fuel_price": fuel_price,
                "mileage": mileage
            }

            db.save_route(result)
            flash("CSV uploaded and route optimized!", "success")

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("upload"))

    return render_template("upload.html", result=result, charts=charts)


@app.route("/history")
def history():
    routes = db.get_all_routes()
    charts = {}
    if routes:
        rg = ReportGenerator(routes)
        charts["distance"] = rg.history_distance_chart()
        charts["cost"]     = rg.history_cost_chart()
    return render_template("history.html", routes=routes, charts=charts)


@app.route("/delete/<int:route_id>", methods=["POST"])
def delete_route(route_id):
    db.delete_route(route_id)
    flash("Route deleted.", "success")
    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(debug=True)