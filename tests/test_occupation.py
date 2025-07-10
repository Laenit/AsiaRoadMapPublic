import os
from objects.occupation.generic_occupation import GenericOccupation
from objects.occupation.activity import Activity
from objects.occupation.housing import Housing


REPO_PATH = os.getcwd()
INPUT_DATA_PATH = os.path.join(REPO_PATH, "tests", "data", "trip_input.json")
OUTPUT_NAME_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "occupation", "output_name.json"
)
OUTPUT_HOUSING_DAYS = os.path.join(
    REPO_PATH, "tests", "data", "output", "occupation", "output_housing_days.json"
)
OUTPUT_ACTIVITY_DAYS = os.path.join(
    REPO_PATH, "tests", "data", "output", "occupation", "output_activity_days.json"
)
OUTPUT_CREATE = os.path.join(
    REPO_PATH, "tests", "data", "output", "occupation", "output_creates.json"
)


def test_it_creates_acitivity():
    activity = Activity(
        "Temple",
        60,
        "Siem Reap",
        None,
        INPUT_DATA_PATH,
        OUTPUT_NAME_DATA_PATH
    )
    activity.create_occupation()

    assert (
        activity.data_file["Siem Reap"]["Activites"]["Temple"]["cost"] == 60
        and not activity.data_file["Siem Reap"]["Activites"]["Temple"]["payement_status"]
    )


def test_it_changes_housing_days():
    housing = Housing(
        "gaga",
        20,
        "Siem Reap",
        None,
        INPUT_DATA_PATH,
        OUTPUT_HOUSING_DAYS
    )
    housing.create_occupation()
    housing.define_days(["Jour 2", "Jour 3"])

    assert (
        housing.data_file["Siem Reap"]["Hebergements"]["gaga"]["day"] == ["Jour 2", "Jour 3"]
    )

    assert (
        housing.data_file["Siem Reap"]["Jour 2"]["Hebergements"]["gaga"]["cost"] == 20
    )


def test_it_changes_activity_days():
    housing = Activity(
        "Bateau",
        30,
        "Siem Reap",
        None,
        INPUT_DATA_PATH,
        OUTPUT_ACTIVITY_DAYS
    )
    housing.create_occupation()
    housing.define_days("Jour 2")

    assert (
        housing.data_file["Siem Reap"]["Activites"]["Bateau"]["day"] == "Jour 2"
    )

    assert (
        housing.data_file["Siem Reap"]["Jour 2"]["Activites"]["Bateau"]["cost"] == 30
    )


def test_it_creates_occupation():
    occupation = GenericOccupation(
        "Taxi",
        5,
        "Repas",
        "Siem Reap",
        "Jour 3",
        INPUT_DATA_PATH,
        OUTPUT_CREATE
    )

    occupation.create_occupation()

    assert (
        not occupation.data_file["Siem Reap"]["Jour 3"]["Repas"]["Taxi"]["payement_status"]
    )


def test_it_changes_cost():
    occupation = GenericOccupation(
        "Taxi",
        5,
        "Repas",
        "Siem Reap",
        "Jour 3",
        INPUT_DATA_PATH,
        OUTPUT_CREATE
    )

    occupation.create_occupation()
    occupation.change_cost(10)

    assert (
        occupation.data_file["Siem Reap"]["Jour 3"]["Repas"]["Taxi"]["cost"] == 10
    )


def test_it_changes_payement_status():
    occupation = GenericOccupation(
        "Taxi",
        5,
        "Repas",
        "Siem Reap",
        "Jour 3",
        INPUT_DATA_PATH,
        OUTPUT_CREATE
    )

    occupation.create_occupation()
    occupation.change_payement_status()

    assert (
        occupation.data_file["Siem Reap"]["Jour 3"]["Repas"]["Taxi"]["payement_status"]
    )
