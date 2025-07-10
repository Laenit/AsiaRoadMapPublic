import os
from objects.occupation.generic_occupation import GenericOccupation

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")


class Housing(GenericOccupation):
    def __init__(
            self,
            name,
            cost,
            place,
            day=None,
            input_data_path=DATA_PATH,
            output_data_path=DATA_PATH
    ):
        super().__init__(name, cost, "Hebergements", place, day, input_data_path, output_data_path)

        self.type = "Hebergements"

        self.path = [place, self.type, name]

    def define_days(self, days):
        if self.day is not None:
            for day in self.day:
                path_previous_day = self.path[:-2] + [day] + self.path[-2:]
                self.delete_item(path_previous_day)
        for day in days:
            path_day = self.path[:-2] + [day] + self.path[-2:]
            information = self.get_information(self.path)
            self.change_value(path=path_day, new_value=information)
        path_day_value = self.path + ["day"]
        self.change_value(days, path=path_day_value)
        self.day = days
