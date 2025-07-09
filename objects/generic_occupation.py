import os
from data.json_utils import load_data, save_data
from generic_object import GenericObejct

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "tests", "trip.json")


class GenericOccupation(GenericObejct):
    def __init__(self, name, cost, type, place):
        super().__init__()
        self.cost = cost
        self.name = name
        self.is_paid = False
        self.type = type
        self.place = place
        self.day = None

        self.path = [self.place][self.type][self.name]

    def get_information(self):
        return self.data_file

    def change_cost(self, new_cost):
        path_cost = self.path + "cost"
        self.change_value(new_cost, path_cost)
        self.cost = new_cost

    def rename(self, new_name):
        path_name = self.path
        self.change_key(new_name, path_name)
        self.name = new_name

    def change_payement_status(self):
        path_payement_status = self.path + "payement_status"
        self.is_paid = not self.is_paid
        self.change_value(self.is_paid, path_payement_status)

    def define_days(self, day):

