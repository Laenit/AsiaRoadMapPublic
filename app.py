import streamlit as st
import folium
from streamlit_folium import st_folium
from travel_times_route import compute_travel_times_and_routes
from utils import format_duration_hm
from data.json_utils import load_data, save_data
from trip import Trip
from kml_mixin import KMLMixin
import time

# --- CONFIG ---
ORS_API_KEY = st.secrets["ORS_API_KEY"]
KML_URL = st.secrets["KML_URL"]
DATA_FILE = "trip.json"

kml_mixin = KMLMixin()

# --- STREAMLIT UI ---
st.set_page_config(page_title="RoadMap des babylove", page_icon="🌍")
st.title("📍 RoadMap des Babylove")

with st.spinner("📥 Chargement et parsing du KML..."):
    if "places" not in st.session_state:
        st.session_state.places = kml_mixin.get_place_from_kml_url(KML_URL)

if not st.session_state.places:
    st.warning(
        "Aucune étape trouvée dans la couche 'Etapes du voyage'."
        " Vérifie l'URL ou la structure KML."
    )
    st.stop()

    # Mise en cache des routes et temps de trajet
    @st.cache_data(show_spinner=False, persist=True)
    def get_travel_times_and_routes(places, api_key):
        return compute_travel_times_and_routes(places, api_key)

    with st.spinner("🧮 Calcul des durées de trajet..."):
        if (
            "travel_times" not in st.session_state
            or "routes_geojson" not in st.session_state
        ):
            travel_times, routes_geojson = get_travel_times_and_routes(
                st.session_state.places, ORS_API_KEY
            )
            st.session_state.travel_times = travel_times
            st.session_state.routes_geojson = routes_geojson
            time.sleep(1.5)

with st.spinner("🧮 Calcul des durées de trajet..."):
    if (
        "travel_times" not in st.session_state
        or "routes_geojson" not in st.session_state
    ):
        travel_times, routes_geojson = compute_travel_times_and_routes(
            st.session_state.places, ORS_API_KEY
        )
        st.session_state.travel_times = travel_times
        st.session_state.routes_geojson = routes_geojson
        time.sleep(1.5)

places = st.session_state.places
travel_times = st.session_state.travel_times
routes_geojson = st.session_state.routes_geojson

total_days = sum(p['days'] for p in places)
total_travel_hours = sum(travel_times)

st.subheader("🚍 Combien de temps on a prévu ?")
st.markdown(f"- Nombre d'étapes : **{len(places)}**")
st.markdown(f"- 🛏️ Durée du voyage sans les trajets : **{total_days}** jours")
st.markdown(
    f"- 🛣️ Temps total estimé de trajet :"
    f"**{format_duration_hm(total_travel_hours)}**"
    f" (~{total_travel_hours/24:.1f} jours)"
)

st.subheader("📆 C'est quoi le plan ?")

data = load_data(DATA_FILE)
trip = Trip(places, data)
trip.get_trip_from_place()
save_data(trip.trip_data, DATA_FILE)

suppression = []

for i, (place, jours) in enumerate(trip.trip_data.items()):
    with st.expander(
        f"**Etape {i+1} - {place}** : {places[i]['days']} jour(s)"
    ):
        for jour, activities in jours.items():
            with st.expander(f"📅 {jour}"):
                for activity, items in activities.items():
                    with st.expander(f"{activity}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_activity = st.text_input(
                                "Nom", key=f"{place},{jour},{activity},txt"
                            )
                        with col2:
                            cost = st.text_input(
                                "Prix ($)", key=f"{place},{jour},{activity},cost"
                            )
                        if st.button(
                            "Ajouter", key=f"{place},{jour},{activity}"
                        ) and new_activity:
                            trip.trip_data[place][jour][activity].append(
                                {
                                    new_activity: int(cost) if cost.isdigit()
                                    else 0
                                }
                            )
                            save_data(trip.trip_data, DATA_FILE)
                            st.success(f"{new_activity} ajouté(e) !")
                        for idx, item in enumerate(
                            trip.trip_data[place][jour][activity]
                        ):
                            name, cost_val = list(item.items())[0]
                            cols = st.columns([1, 4, 2, 1])
                            with cols[0]:
                                st.checkbox(
                                    "", key=f"{place}_{jour}_{activity}_{name}_{idx}"
                                )
                            with cols[1]:
                                st.markdown(f"**{name}**")
                            with cols[2]:
                                st.markdown(f"{cost_val} $")
                            with cols[3]:
                                if st.button(
                                    "🗑️",
                                    key=f"del_{place}_{jour}_{activity}_{name}_{idx}",
                                ):
                                    suppression.append((place, jour, activity, idx))

    if i < len(places) - 1:
        st.markdown(
            f"→ 🚍 Trajet vers **{places[i+1]['city']}**"
            f" : {format_duration_hm(travel_times[i])}"
        )

if suppression:
    for place, jour, act, index in suppression:
        try:
            del trip.trip_data[place][jour][act][index]
        except IndexError:
            pass
    save_data(trip.trip_data, DATA_FILE)
    st.success("✅ Élément(s) supprimé(s) avec succès !")
    st.rerun()

# --- FOLIUM MAP ---
if places[0]['lat'] and places[0]['lon']:
    m = folium.Map(location=[places[0]['lat'], places[0]['lon']], zoom_start=6)
else:
    m = folium.Map(zoom_start=2)

for p in places:
    if p['lat'] and p['lon']:
        folium.Marker(
            location=[p['lat'], p['lon']],
            popup=f"{p['city']}<br>{p['days']} jours",
            tooltip=p['city'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

for i, feature in enumerate(routes_geojson):
    if feature:
        duration = feature['properties'].get('custom_duration')
        if duration is not None and isinstance(duration, (int, float)):
            tooltip_text = f"⏱️ {format_duration_hm(duration)} de trajet"
        else:
            tooltip_text = "⏱️ Durée inconnue de trajet"
        folium.GeoJson(
            data=feature['geometry'],
            style_function=lambda _: {'color': 'red', 'weight': 4, 'opacity': 0.7},
            tooltip=tooltip_text
        ).add_to(m)

st.subheader("🗺️ C'est où qu'elles sont les étapes ?")
st_folium(m, width=700, height=500)
