import os
from objects.generic_object import GenericObejct

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "trip.json")


class GenericOccupation(GenericObejct):
    def __init__(
            self,
            name,
            cost,
            type,
            place,
            day=None,
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

        self.path = [place, day, type, name]

    def create_occupation(self):
        self.change_value(
            {"cost": self.cost, "payement_status": self.is_paid, "day": self.day},
            self.path,
        )

    def change_cost(self, new_cost):
        path_cost = self.path + ["cost"]
        self.change_value(new_cost, path_cost)
        self.cost = new_cost

    def rename(self, new_name):
        path_name = self.path
        self.change_key(new_name, path_name)
        self.name = new_name

    def change_payement_status(self):
        path_payement_status = self.path + ["payement_status"]
        self.is_paid = not self.is_paid
        self.change_value(self.is_paid, path_payement_status)

    def delete_occupation(self):
        self.delete_item(self.path)
