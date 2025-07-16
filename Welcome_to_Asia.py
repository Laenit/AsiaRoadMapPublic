import streamlit as st
from objects.trip import Trip
import os
from utils.utils import format_duration_hm

# --- CONFIG ---
ORS_API_KEY = st.secrets["ORS_API_KEY"]
KML_URL = st.secrets["KML_URL"]
DATA_FILE = os.path.join("data", "trip.json")
ROUTE_FILE = os.path.join("data", "route.json")

trip = Trip(
    DATA_FILE,
    DATA_FILE,
    ROUTE_FILE
)


# --- STREAMLIT UI ---
st.set_page_config(page_title="RoadMap des babylove", page_icon="🌍")
st.title("📍 RoadMap des Babylove")

with st.spinner("📥 Chargement et parsing du KML..."):
    trip.initialize_places(KML_URL)

trip.get_travel_time_and_routes(ORS_API_KEY)

total_days = sum(p['days'] for p in trip.places)
total_travel_hours = sum(trip.travel_times)

st.subheader("🚍 Combien de temps on a prévu ?")
st.markdown(f"- Nombre d'étapes : **{len(trip.places)}**")
st.markdown(f"- 🛏️ Durée du voyage sans les trajets : **{total_days}** jours")
st.markdown(
    f"- 🛣️ Temps total estimé de trajet :"
    f"**{format_duration_hm(total_travel_hours)}**"
    f" (~{total_travel_hours/24:.1f} jours)"
)
