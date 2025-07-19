import os
from objects.generic_object import GenericObejct

REPO_PATH = os.getcwd()
INPUT_DATA_PATH = os.path.join(REPO_PATH, "tests", "data", "trip_input.json")
OUTPUT_KEY_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "generic_object", "output_key.json"
)
OUTPUT_CHANGE_VALUE_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "generic_object", "output_change_value.json"
)
OUTPUT_ADD_VALUE_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "generic_object", "output_add_value.json"
)
OUTPUT_DELETE_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "generic_object", "output_delete.json"
)


def test_it_return_information():
    generic_object = GenericObejct(INPUT_DATA_PATH, INPUT_DATA_PATH)

    assert (
        generic_object.get_information(["Siem Reap", "Jour 1"])
        == generic_object.data_file["Siem Reap"]["Jour 1"]
    )


def test_it_changes_key():
    generic_object = GenericObejct(INPUT_DATA_PATH, OUTPUT_KEY_DATA_PATH)
    key_path = ["Siem Reap", "Jour 1", "Hebergements", "gaga"]
    new_key = "hotel"
    generic_object.change_key(new_key=new_key, path=key_path)

    assert (
        list(generic_object.data_file["Siem Reap"]["Jour 1"]["Hebergements"].keys())
        == [new_key]
    )


def test_it_changes_value():
    generic_object = GenericObejct(INPUT_DATA_PATH, OUTPUT_CHANGE_VALUE_DATA_PATH)
    key_path = ["Siem Reap", "Jour 1", "Hebergements", "gaga"]
    new_value = 30
    generic_object.change_value(new_value=new_value, path=key_path)

    assert (
        generic_object.data_file["Siem Reap"]["Jour 1"]["Hebergements"]["gaga"]
        == 30
    )


def test_change_value_can_add():
    generic_object = GenericObejct(INPUT_DATA_PATH, OUTPUT_ADD_VALUE_DATA_PATH)
    key_path = ["Siem Reap", "Jour 1", "Hebergements", "auberge"]
    new_value = 50
    generic_object.change_value(new_value=new_value, path=key_path)

    assert (
        generic_object.data_file["Siem Reap"]["Jour 1"]["Hebergements"]["auberge"]
        == 50
    )


def test_it_deletes_item():
    generic_object = GenericObejct(INPUT_DATA_PATH, OUTPUT_ADD_VALUE_DATA_PATH)
    path = ["Siem Reap", "Jour 1", "Hebergements", "gaga"]
    generic_object.delete_item(path=path)

    assert (
        "gaga" not in
        list(generic_object.data_file["Siem Reap"]["Jour 1"]["Hebergements"])
    )
