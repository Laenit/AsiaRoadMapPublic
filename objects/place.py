import os
from objects.generic_object import GenericObejct
from objects.day_place_mixin import DayPlaceMixin
import pandas as pd

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")
ROUTE_PATH = os.path.join(REPO_PATH, "data", "route.json")


class Place(GenericObejct, DayPlaceMixin):
    def __init__(self,
                 name,
                 days_number,
                 input_data_path=DATA_PATH,
                 output_data_path=DATA_PATH):
        super().__init__(input_data_path, output_data_path)

        self.input_data_path = input_data_path
        self.output_data_path = output_data_path

        self.name = name
        self.days_number = days_number

        self.cost = None

        self.path = [name]

    def get_type_cost_for_place(self, type):
        return self.get_place_type_cost(type, self.days_number, self.name)

    def get_cost(self):
        return self.get_place_cost(self.days_number, self.name)

    def get_place_days_dataframe(self):
        return self.get_days_dataframe(self.days_number, self.name)

    def get_occupation_dataframe(self):
        costs = []
        days = []
        payement_status = []
        types = []
        names = []
        items = self.get_information(self.path)
        for item, type in items.items():
            if not item.startswith("Jour"):
                for occupation, _ in type.items():
                    occupation_path = self.path + [item, occupation]
                    occupation_informations = self.get_information(occupation_path)
                    costs.append(occupation_informations["cost"])
                    days.append(occupation_informations["day"])
                    payement_status.append(occupation_informations["payement_status"])
                    types.append(item)
                    names.append(occupation)
        return pd.DataFrame(
            {
                "name": names,
                "cost": costs,
                "day": days,
                "payement_status": payement_status,
                "types": types
            }
        )

    def delete_place_for_place(self):
        self.delete_place(self.name)
