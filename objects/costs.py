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
        columns_label = [
            "cost",
            "buyer",
            "category",
        ]
        self.costs_dataframe = pd.DataFrame.from_dict(
            self.data_file,
            orient="index",
            columns=columns_label
        )
        self.costs_dataframe.rename(columns={"cost": "total_cost"}, inplace=True)
        self.costs_dataframe["Marie_cost"] = self.costs_dataframe.apply(
            lambda row: row["total_cost"] if row["buyer"] in ["Marie", "Les deux"] else 0,
            axis=1
        )
        self.costs_dataframe["Tinael_cost"] = self.costs_dataframe.apply(
            lambda row: row["total_cost"] if row["buyer"] in ["Tinaël", "Les deux"] else 0,
            axis=1
        )
        return self.costs_dataframe
