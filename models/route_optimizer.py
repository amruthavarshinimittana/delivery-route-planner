from models.route import Route

class RouteOptimizer:
    def __init__(self, stops):
        self.stops = stops

    def dist(self, a, b):
        return abs(a.distance_from_depot - b.distance_from_depot)

    def total_route_distance(self, order):
        total = order[0].distance_from_depot
        for i in range(len(order) - 1):
            total += self.dist(order[i], order[i+1])
        total += order[-1].distance_from_depot
        return round(total, 2)

    def unoptimized_distance(self):
        return self.total_route_distance(self.stops)

    def optimize(self, fuel_price=100.0, mileage=12.0):
        if not self.stops:
            return Route([], fuel_price, mileage, 0)

        unvisited = self.stops[:]
        ordered = []
        current_dist = 0.0

        while unvisited:
            nearest = min(unvisited,
                         key=lambda s: abs(s.distance_from_depot - current_dist))
            ordered.append(nearest)
            current_dist = nearest.distance_from_depot
            unvisited.remove(nearest)

        opt_dist = self.total_route_distance(ordered)
        return Route(ordered, fuel_price, mileage, opt_dist)