import os
from objects.day import Day

REPO_PATH = os.getcwd()
INPUT_DATA_PATH = os.path.join(REPO_PATH, "tests", "data", "trip_input.json")
OUTPUT_DF_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "day", "output_df.json"
)
OUTPUT_COST_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "day", "output_cost.json"
)


def test_it_returns_dataframe():
    day = Day("Siem Reap", 1, 10, INPUT_DATA_PATH, OUTPUT_DF_DATA_PATH)
    df = day.get_type_dataframe("Hebergements")

    assert (df["name"] == "gaga").any()


def test_it_returns_type_cost():
    day = Day("Siem Reap", 1, 10, INPUT_DATA_PATH, OUTPUT_DF_DATA_PATH)
    activity_cost = day.get_type_cost(type="Activites")
    housing_cost = day.get_type_cost(type="Hebergements")

    assert activity_cost == 60 and housing_cost == 20


def test_it_returns_total_cost():
    day = Day("Siem Reap", 1, 10, INPUT_DATA_PATH, OUTPUT_DF_DATA_PATH)
    total_cost = day.get_total_cost()

    assert total_cost == 100
