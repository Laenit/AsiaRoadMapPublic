import os
from objects.generic_object import GenericObejct
from objects.day_place_mixin import DayPlaceMixin
from utils.kml_mixin import KMLMixin
from utils.json_utils import load_data, save_data
from utils.travel_times_route import compute_travel_time_and_route
import time
import pandas as pd

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")
ROUTE_PATH = os.path.join(REPO_PATH, "data", "route.json")


class Trip(GenericObejct, KMLMixin, DayPlaceMixin):
    def __init__(self,
                 input_data_path=DATA_PATH,
                 output_data_path=DATA_PATH,
                 route_path=ROUTE_PATH
                 ):
        super().__init__(input_data_path, output_data_path)

        self.route_path = route_path

        self.places = None
        self.travel_times = None
        self.routes_geojson = None

    def initialize_places(self, url):
        self.places = self.get_place_from_kml_url(url)

    def get_places_from_file(self):
        self.places = load_data(self.route_path)["places"]

    def get_trip_from_place(self):
        existing_cities = []
        for city in self.data_file:
            existing_cities.append(city)
        for place in self.places:
            if place['city'] not in existing_cities:
                self.create_place(place["city"], place["days"])

    def get_travel_time_and_routes(self, ors_api_key):
        # --- Charger ou initialiser les données de route.json ---
        if os.path.exists(self.route_path):
            route_data = load_data(self.route_path)
            self.places = route_data.get("places", [])
            self.travel_times = route_data.get("travel_times", [])
            self.routes_geojson = route_data.get("routes_geojson", [])
        else:
            route_data = {}
            self.places = []
            self.travel_times = []
            self.routes_geojson = []

        # --- Calculer les trajets manquants ---
        for i in range(len(self.places) - 1):
            from_place = self.places[i]
            to_place = self.places[i + 1]

            # Vérifier si déjà calculé et valide
            if (
                self.travel_times[i] is not None
                and self.travel_times[i] > 0
                and self.routes_geojson[i] is not None
            ):
                continue

            travel_time, route_geojson = compute_travel_time_and_route(
                from_place, to_place, ors_api_key
            )
            self.travel_times[i] = travel_time
            self.routes_geojson[i] = route_geojson

            # Sauvegarder après chaque étape pour ne rien perdre
            save_data({
                "places": self.places,
                "travel_times": self.travel_times,
                "routes_geojson": self.routes_geojson
            }, self.route_path)

            time.sleep(0.5)

    def get_places_dataframe(self):
        costs = []
        names = []
        places_days = []
        for data in self.places:
            name = data["city"]
            days = data["days"]
            cost = self.get_place_cost(days, name)
            costs.append(cost)
            names.append(name)
            places_days.append(days)
        return pd.DataFrame(
            {
                "name": names,
                "number_of_days": places_days,
                "cost": costs
            }
        )

    def get_day_trip_number(self, place, day_number):
        counter = 0
        selected_place = self.places[0]
        idx_place = 0
        while selected_place["city"] != place:
            counter += selected_place["days"]
            idx_place += 1
            selected_place = self.places[idx_place]
        return counter + day_number

    def get_trip_days_dataframe(self):
        final_dataframe = pd.DataFrame({})
        for data in self.places:
            place_df = self.get_days_dataframe(data["days"], data["city"])
            place_df["place"] = [data["city"]] * data["days"]
            final_dataframe = pd.concat([final_dataframe, place_df])
        print(final_dataframe)
        final_dataframe["day_number_trip"] = final_dataframe.apply(
            lambda row: self.get_day_trip_number(row["place"], row["day_number"]), axis=1
        )
        return final_dataframe
