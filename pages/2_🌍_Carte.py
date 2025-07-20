import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.utils import format_duration_hm
from objects.trip import Trip

trip = Trip()
trip.get_places_from_file()
trip.get_trip_from_place()
trip.get_travel_time_and_routes_from_file()

# --- FOLIUM MAP ---
if trip.places[0]['lat'] and trip.places[0]['lon']:
    m = folium.Map(
        location=[trip.places[0]['lat'], trip.places[0]['lon']],
        zoom_start=6,
        tiles="CartoDB Voyager",
    )
else:
    m = folium.Map(zoom_start=2)

for p in trip.places:
    if p['lat'] and p['lon']:
        folium.Marker(
            location=[p['lat'], p['lon']],
            popup=f"{p['city']}<br>{p['days']} jours",
            tooltip=p['city'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

for i, feature in enumerate(trip.routes_geojson):
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
