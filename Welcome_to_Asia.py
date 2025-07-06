import streamlit as st
from travel_times_route import compute_travel_time_and_route
from utils import format_duration_hm
from data.json_utils import load_data, save_data
import os
from kml_mixin import KMLMixin
import time

# --- CONFIG ---
ORS_API_KEY = st.secrets["ORS_API_KEY"]
KML_URL = st.secrets["KML_URL"]
DATA_FILE = "trip.json"
ROUTE_FILE = "route.json"

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

places = st.session_state.places

# --- Charger ou initialiser les données de route.json ---
if os.path.exists(ROUTE_FILE):
    route_data = load_data(ROUTE_FILE)
    cached_places = route_data.get("places", [])
    cached_travel_times = route_data.get("travel_times", [])
    cached_routes_geojson = route_data.get("routes_geojson", [])
else:
    route_data = {}
    cached_places = []
    cached_travel_times = []
    cached_routes_geojson = []

# --- Initialiser les listes si tailles différentes ---
if len(cached_places) != len(places):
    cached_places = places
    cached_travel_times = [None] * (len(places) - 1)
    cached_routes_geojson = [None] * (len(places) - 1)

# --- Calculer les trajets manquants ---
for i in range(len(places) - 1):
    from_place = places[i]
    to_place = places[i + 1]

    # Vérifier si déjà calculé et valide
    if (
        cached_travel_times[i] is not None
        and cached_travel_times[i] > 0
        and cached_routes_geojson[i] is not None
    ):
        st.spinner(f"✅ Étape {i+1} déjà en cache : {from_place['city']} ➡️ {to_place['city']}")
        continue  # sauter cette étape

    # Calculer la route avec ORS
    with st.spinner(
        f"📡 Calcul du trajet pour l'étape {i+1}: {from_place['city']} ➡️ {to_place['city']}"
    ):
        try:
            travel_time, route_geojson = compute_travel_time_and_route(
                from_place, to_place, ORS_API_KEY
            )
            cached_travel_times[i] = travel_time
            cached_routes_geojson[i] = route_geojson

            # Sauvegarder après chaque étape pour ne rien perdre
            save_data({
                "places": places,
                "travel_times": cached_travel_times,
                "routes_geojson": cached_routes_geojson
            }, ROUTE_FILE)

            time.sleep(1)  # petite pause pour éviter de saturer l'API
        except Exception as e:
            st.error(f"❌ Erreur lors du calcul de l'étape {i+1}: {e}")
            cached_travel_times[i] = 0  # marquer comme échec pour tenter plus tard

# --- Stocker dans session_state ---
st.session_state.travel_times = cached_travel_times
st.session_state.routes_geojson = cached_routes_geojson

total_days = sum(p['days'] for p in places)
total_travel_hours = sum(cached_travel_times)

st.subheader("🚍 Combien de temps on a prévu ?")
st.markdown(f"- Nombre d'étapes : **{len(places)}**")
st.markdown(f"- 🛏️ Durée du voyage sans les trajets : **{total_days}** jours")
st.markdown(
    f"- 🛣️ Temps total estimé de trajet :"
    f"**{format_duration_hm(total_travel_hours)}**"
    f" (~{total_travel_hours/24:.1f} jours)"
)
