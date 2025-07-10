import os
from objects.generic_object import GenericObejct
import pandas as pd

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")


class Day(GenericObejct):
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

        self.path = [place, "Jour" + f" {number_place}"]

    def get_type_dataframe(self, type):
        type_path = self.path + [type]
        occupations = self.get_information(type_path)
        costs = []
        payement_status = []
        names = []
        for occupation, _ in occupations.items():
            occupation_path = type_path + [occupation]
            occupation_informations = self.get_information(occupation_path)
            costs.append(occupation_informations["cost"])
            payement_status.append(occupation_informations["payement_status"])
            names.append(occupation)
        return pd.DataFrame({"cost": costs, "name": names, "payement_status": payement_status})

    def get_type_cost(self, type):
        dataframe = self.get_type_dataframe(type)
        return dataframe["cost"].sum()

    def get_total_cost(self):
        types = self.get_information(self.path)
        total = 0
        for type in types:
            total += self.get_type_cost(type)
        return total
