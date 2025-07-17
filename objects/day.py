import os
from objects.generic_object import GenericObejct
from objects.day_place_mixin import DayPlaceMixin

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")


class Day(GenericObejct, DayPlaceMixin):
    def __init__(self,
                 place,
                 number_place,
                 number_trip,
                 input_data_path=DATA_PATH,
                 output_data_path=DATA_PATH):
        super().__init__(input_data_path, output_data_path)

        self.place = place
        self.number_place = number_place
        self.number_trip = number_trip

        self.cost = None

        self.name = f"Jour {number_place}"

        self.path = [place, f"Jour {number_place}"]

    def get_day_type_dataframe(self, type):
        return self.get_type_dataframe(type, self.path)

    def get_day_type_cost(self, type):
        return self.get_type_cost(type, self.path)

    def get_day_total_cost(self):
        return self.get_total_cost(self.path)
