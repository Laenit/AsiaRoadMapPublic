import os
from objects.occupation.generic_occupation import GenericOccupation

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")


class Activity(GenericOccupation):
    def __init__(
            self,
            name,
            cost,
            type,
            place,
            day=None,
            input_data_path=DATA_PATH,
            output_data_path=DATA_PATH
    ):
        super().__init__(name, cost, type, place, day, input_data_path, output_data_path)

    def define_days(self, day):
        if self.day is not None:
            path_previous_day = self.path[:-2] + self.day + self.path[-2:]
            self.delete_item(path_previous_day)
        path_day = self.path[:-2] + day + self.path[-2]
        self.change_value(path=path_day, new_value=self.name)
        path_day_value = self.path + "day"
        self.change_value(day, path=path_day_value)
        self.day = day
