import os
import pandas as pd
from objects.generic_object import GenericObejct

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "data", "costs.json")


class Costs(GenericObejct):
    def __init__(self,
                 input_data_path=DATA_PATH,
                 output_data_path=DATA_PATH,
                 ):
        super().__init__(input_data_path, output_data_path)

        self.costs_dataframe = None

    def create_cost(self, cost_name, cost, buyer, category):
        path = [cost_name]
        self.change_value({"cost": cost, "buyer": buyer, "category": category}, path)

    def delete_cost(self, cost_name):
        path = [cost_name]
        self.delete_item(path)

    def get_costs_dataframe(self):
        names = []
        costs = []
        buyers = []
        categories = []
        for name, data in self.data_file.items():
            names.append(name)
            costs.append(data["cost"])
            buyers.append(data["buyer"])
            categories.append(data["category"])
        self.costs_dataframe = pd.DataFrame({"cost": costs, "buyer": buyers, "category": categories})
        return self.costs_dataframe
