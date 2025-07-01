import json


def load_data(data_file):
    with open(data_file, "r") as f:
        return json.load(f)


def save_data(data, data_file):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)
