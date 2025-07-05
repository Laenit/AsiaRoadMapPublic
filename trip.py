class Trip():
    def __init__(self, places, json_data_file):
        self.places = places
        self.trip_data = json_data_file

    def get_trip_from_place(self):
        existing_cities = []
        for city in self.trip_data:
            existing_cities.append(city)
        for place in self.places:
            if place['city'] not in existing_cities:
                days = {
                    "Jours": {},
                    "Activites": [],
                    "Hebergements": [],
                }
                for i in range(place["days"]):
                    days["Jours"][f"Jour {i+1}"] = {
                        "Activites": [],
                        "Repas": [],
                        "Transports": [],
                        "Hebergements": [],
                    }
                self.trip_data[
                    f"{place['city']}"
                ] = days
        return self.trip_data
