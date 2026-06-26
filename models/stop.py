class Stop:
    def __init__(self, stop_id, name, distance_from_depot):
        self.stop_id = stop_id
        self.name = name
        self.distance_from_depot = float(distance_from_depot)

    def to_dict(self):
        return {
            "stop_id": self.stop_id,
            "name": self.name,
            "distance_from_depot": self.distance_from_depot
        }

    def __repr__(self):
        return f"Stop({self.name}, {self.distance_from_depot} km)"