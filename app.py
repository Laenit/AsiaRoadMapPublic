import streamlit as st
import folium
from streamlit_folium import st_folium
from travel_times_route import compute_travel_times_and_routes
from utils import format_duration_hm
from kml_mixin import KMLMixin

# --- CONFIG ---
ORS_API_KEY = st.secrets["ORS_API_KEY"]
KML_URL = st.secrets["KML_URL"]


kml_mixin = KMLMixin()


# --- STREAMLIT UI ---
st.set_page_config(page_title="RoadMap des babylove", page_icon="🌍")
st.title("📍 RoadMap des babylove")

if st.button("🔁 Mettre à jour l'itinéraire"):

    with st.spinner("📥 Chargement et parsing du KML..."):
        st.session_state.places = kml_mixin.get_place_from_kml_url(KML_URL)

    if not st.session_state.places:
        st.warning(
            "Aucune étape trouvée dans la couche 'Etapes du voyage'."
            " Vérifie l'URL ou la structure KML."
            )
    else:
        with st.spinner("🧮 Calcul des durées de trajet..."):
            (
                st.session_state.travel_times,
                st.session_state.routes_geojson,
            ) = compute_travel_times_and_routes(
                st.session_state.places, ORS_API_KEY
            )

# --- AFFICHAGE ---
if "places" in st.session_state and st.session_state.places:
    places = st.session_state.places
    travel_times = st.session_state.travel_times
    routes_geojson = st.session_state.routes_geojson

    total_days = sum(p['days'] for p in places)
    total_travel_hours = sum(travel_times)

    st.subheader("🚍 Combien de temps on a prévu ?")
    st.markdown(f"- Nombre d'étapes : **{len(places)}**")
    st.markdown(
        f"- 🛏️ Durée du voyage sans les trajets : **{total_days}** jours"
        )
    st.markdown(
        f"- 🛣️ Temps total estimé de"
        f"trajet : **{format_duration_hm(total_travel_hours)}**"
        f"(~{total_travel_hours/24:.1f} jours)"
    )

    st.subheader("📆 C'est quoi le plan ?")
    for i, place in enumerate(places):
        st.markdown(
            f"🛏️ **Étape {i+1} : {place['city']}** - {place['days']} jours"
        )
        if i < len(places)-1:
            st.markdown(
                f"→ 🚍 Trajet vers **{places[i+1]['city']}**"
                f" : {format_duration_hm(travel_times[i+1])}"
            )

    # --- FOLIUM MAP ---
    if places[0]['lat'] and places[0]['lon']:
        m = folium.Map(
            location=[places[0]['lat'], places[0]['lon']], zoom_start=6
        )
    else:
        m = folium.Map(zoom_start=2)

    # Marqueurs
    for p in places:
        if p['lat'] and p['lon']:
            folium.Marker(
                location=[p['lat'], p['lon']],
                popup=f"{p['city']}<br>{p['days']} jours",
                tooltip=p['city'],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

    # Lignes de trajet avec durée en popup
    for i, feature in enumerate(routes_geojson):
        if feature:
            duration = feature['properties'].get('custom_duration', '?')
            folium.GeoJson(
                data=feature['geometry'],
                style_function=lambda x: {
                    'color': 'red', 'weight': 4, 'opacity': 0.7
                },
                tooltip=f"⏱️ {format_duration_hm(duration)} de trajet"
            ).add_to(m)

    st.subheader("🗺️ C'est où qu'elles sont les étapes ?")
    st_folium(m, width=700, height=500)
