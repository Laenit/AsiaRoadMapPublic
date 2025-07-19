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
        self.general_change(self.change_value, {"cost": self.cost, "payement_status": self.is_paid, "day": self.day})

    def change_cost(self, new_cost):
        self.general_change(self.change_value, new_cost, ["cost"])

    def rename(self, new_name):
        self.general_change(self.change_key, new_name)

    def change_payement_status(self):
        self.is_paid = not self.is_paid
        self.general_change(self.change_value, self.is_paid, ["payement_status"])

    def delete_occupation(self):
        if self.day is not None:
            if not isinstance(self.day, list):
                self.delete_item(self.path)
            else:
                for day in self.day:
                    path_day = self.path_general[:-2] + [day] + self.path_general[-2:]
                    self.delete_item(path_day)
        if self.general:
            self.delete_item(self.path_general)

    def general_change(self, function, new_value, path_precision=False):
        if not path_precision:
            if self.day is not None:
                if not isinstance(self.day, list):
                    function(new_value, self.path)
                else:
                    for day in self.day:
                        path_day = self.path_general[:-2] + [day] + self.path_general[-2:]
                        function(new_value, path_day)
            if self.general:
                function(new_value, self.path_general)
        else:
            if self.day is not None:
                if not isinstance(self.day, list):
                    function(new_value, self.path + path_precision)
                else:
                    for day in self.day:
                        path_day = self.path_general[:-2] + [day] + self.path_general[-2:] + path_precision
                        function(new_value, path_day)
            if self.general:
                function(new_value, self.path_general + path_precision)

    def define_activity_days(self, day):
        if self.day is not None:
            path_previous_day = self.path
            self.delete_item(path_previous_day)
        if day is not None:
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
