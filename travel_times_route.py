import streamlit as st
import openrouteservice


def compute_travel_times_and_routes(
        places, ors_api_key, profile='driving-hgv'
):
    client = openrouteservice.Client(key=ors_api_key)
    travel_times = [0]  # 0 h pour départ
    routes_geojson = []

    for i in range(1, len(places)):
        prev = places[i-1]
        curr = places[i]
        if None in (prev['lon'], prev['lat'], curr['lon'], curr['lat']):
            travel_times.append(0)
            routes_geojson.append(None)
            continue
        coords = [
            (prev['lon'], prev['lat']),
            (curr['lon'], curr['lat'])
        ]
        try:
            route = client.directions(
                coords, profile=profile, format='geojson'
            )
            duration_sec = route['features'][0]['properties']['segments'][0][
                'duration'
            ]
            travel_times.append(round(duration_sec / 3600, 2))
            route['features'][0]['properties']['custom_duration'] = round(
                duration_sec / 3600, 2
            )
            routes_geojson.append(route['features'][0])
        except Exception as e:
            st.warning(f"Erreur ORS pour étape {i}: {e}")
            travel_times.append(0)
            routes_geojson.append(None)
    return travel_times, routes_geojson
