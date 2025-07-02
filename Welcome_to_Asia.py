import streamlit as st
from travel_times_route import compute_travel_times_and_routes
from utils import format_duration_hm
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
