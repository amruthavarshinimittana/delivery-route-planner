class CostCalculator:
    def __init__(self, fuel_price_per_litre=100.0, mileage_kmpl=12.0, driver_cost_per_hour=50.0):
        self.fuel_price_per_litre = fuel_price_per_litre
        self.mileage_kmpl = mileage_kmpl
        self.driver_cost_per_hour = driver_cost_per_hour

    def fuel_cost(self, distance_km):
        litres = distance_km / self.mileage_kmpl
        return round(litres * self.fuel_price_per_litre, 2)

    def driver_cost(self, time_hours):
        return round(time_hours * self.driver_cost_per_hour, 2)

    def total_cost(self, distance_km, time_hours):
        return round(self.fuel_cost(distance_km) + self.driver_cost(time_hours), 2)

    def cost_breakdown(self, distance_km, time_hours):
        return {
            "fuel_cost": self.fuel_cost(distance_km),
            "driver_cost": self.driver_cost(time_hours),
            "total_cost": self.total_cost(distance_km, time_hours),
            "litres_used": round(distance_km / self.mileage_kmpl, 2)
        }