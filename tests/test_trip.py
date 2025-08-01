import os
from objects.trip import Trip
from utils.json_utils import load_data
import streamlit as st

REPO_PATH = os.getcwd()
INPUT_DATA_PATH = os.path.join(REPO_PATH, "tests", "data", "trip_input.json")
INPUT_ROUTE_PATH = os.path.join(REPO_PATH, "tests", "data", "route_input.json")
OUTPUT_DATA_PATH = os.path.join(
    REPO_PATH, "tests", "data", "output", "trip", "trip_output.json"
)
FULL_OUTPUT_PATH = os.path.join(REPO_PATH, "tests", "data", "output", "trip", "full_trip.json")


def test_it_initializes_places():
    trip = Trip(
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH,
        INPUT_ROUTE_PATH
    )
    trip.initialize_places(url=st.secrets["KML_URL"])

    assert (
        trip.places[0]["city"] == "Bangkok"
    )


def test_it_initialise_trip():
    trip = Trip(
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH,
        INPUT_ROUTE_PATH
    )
    trip.get_places_from_file()
    trip.get_trip_from_place()

    assert (
        "Bangkok" in list(trip.data_file.keys())
    )

    assert (
        "Jour 1" in list(trip.data_file["Bangkok"].keys())
    )


def test_it_create_route_file():
    trip = Trip(
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH,
        INPUT_ROUTE_PATH
    )
    trip.get_places_from_file()
    trip.get_travel_time_and_routes(st.secrets["ORS_API_KEY"])

    assert (
        load_data(INPUT_ROUTE_PATH)["places"][0]["city"] == "Bangkok"
    )


def test_it_returns_places_dataframe():
    trip = Trip(
        INPUT_DATA_PATH,
        FULL_OUTPUT_PATH,
        INPUT_ROUTE_PATH
    )
    trip.get_places_from_file()
    trip.get_trip_from_place()

    df = trip.get_places_dataframe()

    assert (
        df["cost"].count() == 8
    )


def test_it_returns_day_trip_number():
    trip = Trip(
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH,
        INPUT_ROUTE_PATH
    )
    trip.get_places_from_file()
    trip.get_trip_from_place()

    number = trip.get_day_trip_number("Siem Reap", 2)

    assert (
        number == 3
    )


def test_it_returns_days_trip_dataframe():
    trip = Trip(
        INPUT_DATA_PATH,
        OUTPUT_DATA_PATH,
        INPUT_ROUTE_PATH
    )
    trip.get_places_from_file()
    trip.get_trip_from_place()

    df = trip.get_trip_days_dataframe()

    assert (
        df["day"].count() == 21
    )

    assert (
        df["day_number_trip"].iloc[-1] == 21
    )
