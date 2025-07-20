import os
from objects.costs import Costs

REPO_PATH = os.getcwd()
INPUT_DATA_PATH = os.path.join(REPO_PATH, "tests", "data", "costs_input.json")
OUTPUT_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "costs", "costs_output.json"
)


def test_it_creates_cost():
    costs = Costs(
        input_data_path=INPUT_DATA_PATH,
        output_data_path=OUTPUT_DATA_PATH,
    )
    costs.create_cost(
        "Tente",
        20,
        "Marie",
        "Equipement"
    )

    assert (
        "Tente" in costs.data_file.keys()
    )

    assert (
        costs.data_file["Tente"]["cost"] == 20
    )


def test_it_returns_costs_dataframe():
    costs = Costs(
        input_data_path=INPUT_DATA_PATH,
        output_data_path=OUTPUT_DATA_PATH,
    )
    costs.create_cost(
        "Tente",
        20,
        "Marie",
        "Equipement"
    )
    costs.create_cost(
        "Sac",
        100,
        "Tinael",
        "Equipement"
    )
    costs.get_costs_dataframe()

    assert (
        costs.costs_dataframe["cost"].sum() == 120
    )
