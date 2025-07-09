import os
from objects.generic_object import GenericObejct

REPO_PATH = os.getcwd()
DATA_PATH = os.path.join(REPO_PATH, "tests", "trip.json")


def test_it_return_information():
    generic_object = GenericObejct(DATA_PATH)

    assert (
        generic_object.get_information(["Bangkok", "Jours", "Jour 1"])
        == generic_object.data_file["Bangkok"]["Jours"]["Jour 1"]
    )

def test_it_changes_key():
    generic_object = GenericObejct(DATA_PATH)

    assert (
        generic_object.get_information(["Bangkok", "Jours", "Jour 1"])
        == generic_object.data_file["Bangkok"]["Jours"]["Jour 1"]
    )
