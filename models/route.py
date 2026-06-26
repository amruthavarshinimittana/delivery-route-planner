class Route:
    def __init__(self, stops, fuel_price_per_litre=100.0, mileage_kmpl=12.0, real_distance=None):
        self.stops = stops
        self.fuel_price_per_litre = fuel_price_per_litre
        self.mileage_kmpl = mileage_kmpl
        self._real_distance = real_distance

    def total_distance(self):
        if self._real_distance is not None:
            return round(self._real_distance, 2)
        return 0.0

    def estimated_time_hours(self, avg_speed_kmph=40):
        return round(self.total_distance() / avg_speed_kmph, 2)

    def fuel_cost(self):
        litres = self.total_distance() / self.mileage_kmpl
        return round(litres * self.fuel_price_per_litre, 2)

    def stop_names(self):
        return [s.name for s in self.stops]

    def to_dict(self):
        return {
            "stops": [s.name for s in self.stops],
            "total_distance": self.total_distance(),
            "estimated_time_hours": self.estimated_time_hours(),
            "fuel_cost": self.fuel_cost()
        }