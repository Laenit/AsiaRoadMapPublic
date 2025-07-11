import os
from objects.place import Place

REPO_PATH = os.getcwd()
INPUT_DATA_PATH = os.path.join(REPO_PATH, "tests", "data", "trip_input.json")
OUTPUT_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "generic_object", "output.json"
)


def test_it_returns_total_cost():
    place = Place(
        "Siem Reap",
        5,
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH
    )
    place_cost = place.get_place_cost()

    assert (
        place_cost == 130
    )


def test_it_returns_days_dataframe():
    place = Place(
        "Siem Reap",
        5,
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH
    )

    df = place.get_days_dataframe()

    assert (
        df["cost"].sum() == 130
    )


def test_it_returns_occuaption_dataframe():
    place = Place(
        "Siem Reap",
        5,
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH
    )

    df = place.get_occupation_dataframe()

    assert (
        df["cost"].sum() == 50
    )
