import os
from objects.generic_object import GenericObejct

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")


class Occupation(GenericObejct):
    def __init__(
            self,
            name,
            cost,
            type,
            place,
            day=None,
            general=False,
            input_data_path=DATA_PATH,
            output_data_path=DATA_PATH,
            ):
        super().__init__(input_data_path, output_data_path)
        self.cost = cost
        self.name = name
        self.is_paid = False
        self.type = type
        self.place = place
        self.day = day
        self.general = general

        self.path = [place, day, type, name]
        self.path_general = [place, type, name]

    def create_occupation(self):
        if self.day is not None:
            self.change_value(
                {"cost": self.cost, "payement_status": self.is_paid, "day": self.day},
                self.path,
            )
        if self.general:
            self.change_value(
                {"cost": self.cost, "payement_status": self.is_paid, "day": self.day},
                self.path_general,
            )

    def change_cost(self, new_cost):
        if self.day is not None:
            path_cost = self.path + ["cost"]
            self.change_value(new_cost, path_cost)
        if self.general:
            path_cost = self.path_general + ["cost"]
            self.change_value(new_cost, path_cost)
        self.cost = new_cost

    def rename(self, new_name):
        if self.day is not None:
            path_name = self.path
            self.change_key(new_name, path_name)
        if self.general:
            path_name = self.path_general
            self.change_key(new_name, path_name)
        self.name = new_name

    def change_payement_status(self):
        if self.day is not None:
            path_payement_status = self.path + ["payement_status"]
            self.is_paid = not self.is_paid
        if self.general:
            path_payement_status = self.path_general + ["payement_status"]
            self.is_paid = not self.is_paid
        self.change_value(self.is_paid, path_payement_status)

    def delete_occupation(self):
        if self.day is not None:
            self.delete_item(self.path)
        if self.general:
            self.delete_item(self.path_general)

    def define_activity_days(self, day):
        if self.day is not None:
            path_previous_day = self.path
            self.delete_item(path_previous_day)
        path_day = self.path_general[:-2] + [day] + self.path_general[-2:]
        informations = self.get_information(self.path_general)
        self.change_value(new_value=informations, path=path_day)
        path_day_value = self.path_general + ["day"]
        self.change_value(day, path=path_day_value)
        self.day = day

    def define_housing_days(self, days):
        if self.day is not None:
            for day in self.day:
                path_previous_day = self.path_general[:-2] + [day] + self.path_general[-2:]
                self.delete_item(path_previous_day)
        path_day_value = self.path_general + ["day"]
        self.change_value(days, path=path_day_value)
        for day in days:
            path_day = self.path_general[:-2] + [day] + self.path_general[-2:]
            information = self.get_information(self.path_general)
            self.change_value(new_value=information, path=path_day)
        self.day = days
