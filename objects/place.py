import os
from objects.day import Day
from objects.generic_object import GenericObejct
import pandas as pd

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")


class Place(GenericObejct):
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

    def create_place(self):
        for i in range(self.days_number):
            day = Day(
                self.name,
                i + 1,
                None,
                self.input_data_path,
                self.output_data_path,
            )
            day.create_day()
        for occupation in ["Activites", "Hebergements"]:
            self.change_value(
                {},
                self.path + [occupation]
            )

    def get_place_type_cost(self, type):
        type_cost = 0
        for i in range(self.days_number):
            day = Day(
                self.name,
                i + 1,
                None,
                self.input_data_path,
                self.output_data_path,
            )
            type_cost += day.get_type_cost(type)
        return type_cost

    def get_place_cost(self):
        types = ["Activites", "Repas", "Transports", "Hebergements"]
        total = 0
        for type in types:
            total += self.get_place_type_cost(type)
        self.cost = total
        return total

    def get_days_dataframe(self):
        costs = []
        days = []
        for i in range(self.days_number):
            day = Day(
                self.name,
                i + 1,
                None,
                self.input_data_path,
                self.output_data_path
            )
            costs.append(day.get_total_cost())
            days.append(f"Jour {i + 1}")
        return pd.DataFrame({"Day": days, "cost": costs})
    
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
