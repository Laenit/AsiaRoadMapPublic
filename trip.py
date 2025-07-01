import streamlit as st


class Trip():
    def __init__(self, places, json_data_file):
        self.places = places
        self.trip_data = json_data_file

    def get_trip_from_place(self):
        existing_cities = []
        for city in self.trip_data:
            existing_cities.append(city)
            st.markdown(existing_cities)
        for place in self.places:
            if place['city'] not in existing_cities:
                days = {}
                for i in range(place["days"]):
                    days[f"Jour {i+1}"] = {
                        "Activites": [],
                        "Repas": [],
                        "Transports": [],
                    }
                self.trip_data[
                    f"{place['city']}"
                ] = days
        return self.trip_data
