import pandas as pd


class DayPlaceMixin:
    def create_day(self, path):
        self.change_value(
            {
                "Activites": {},
                "Repas": {},
                "Transports": {},
                "Hebergements": {}
            },
            path
        )

    def create_place(self, name, days_number):
        self.change_value(
            {},
            [name]
        )
        for i in range(days_number):
            self.create_day([name, f"Jour {i + 1}"])
        for occupation in ["Activites", "Hebergements"]:
            self.change_value(
                {},
                [name] + [occupation]
            )

    def get_type_dataframe(self, type, path_day):
        type_path = path_day + [type]
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

    def get_type_cost(self, type, path_day):
        dataframe = self.get_type_dataframe(type, path_day)
        return dataframe["cost"].sum()

    def get_total_cost(self, path_day):
        types = self.get_information(path_day)
        total = 0
        for type in types:
            total += self.get_type_cost(type, path_day)
        self.cost = total
        return total

    def get_place_cost(self, days_number, name):
        types = ["Activites", "Repas", "Transports", "Hebergements"]
        total = 0
        for type in types:
            total += self.get_place_type_cost(type, days_number, name)
        self.cost = total
        return total

    def get_days_dataframe(self, days_number, name):
        costs = []
        days = []
        days_numbers = []
        for i in range(days_number):
            costs.append(self.get_total_cost([name, f"Jour {i + 1}"]))
            days.append(f"Jour {i + 1}")
            days_numbers.append(i + 1)
        return pd.DataFrame({"day": days, "cost": costs, "day_number": days_numbers})

    def get_place_type_cost(self, type, days_number, name):
        type_cost = 0
        for i in range(days_number):
            type_cost += self.get_type_cost(type, [name, f"Jour {i + 1}"])
        return type_cost
