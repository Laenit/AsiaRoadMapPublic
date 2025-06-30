import streamlit as st
import requests
import xml.etree.ElementTree as ET
import re
from io import BytesIO
import openrouteservice
import folium
from streamlit_folium import st_folium

# --- CONFIG --- 
ORS_API_KEY = st.secrets["ORS_API_KEY"]
KML_URL = "https://www.google.com/maps/d/kml?mid=1HbOpF1GZloSX8-ayF3TH4Tg0Ixa5LZw&forcekml=1"

def strip_ns(tag):
    return tag.split('}')[-1]

def parse_kml_from_url(url, layer_name_keyword="etapes"):
    response = requests.get(url)
    if not response.ok:
        st.error("Erreur lors du téléchargement du KML")
        return []

    kml_data = BytesIO(response.content)
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    tree = ET.parse(kml_data)
    root = tree.getroot()

    places = []
    for folder in root.iter():
        if strip_ns(folder.tag) == "Folder":
            folder_name = folder.findtext('kml:name', default='', namespaces=ns)
            folder_clean = folder_name.strip().lower()
            if layer_name_keyword in folder_clean:
                for placemark in folder.findall('.//kml:Placemark', namespaces=ns):
                    name = placemark.findtext('kml:name', default='(sans nom)', namespaces=ns)
                    desc = placemark.findtext('kml:description', default='', namespaces=ns)
                    coords_text = placemark.findtext('.//kml:coordinates', default='', namespaces=ns)
                    coords_text = coords_text.strip()
                    try:
                        lon, lat, *_ = map(float, coords_text.split(','))
                    except Exception:
                        lon = lat = None

                    match = re.search(r"(\d+)\s*(j|jour|jours)", desc.lower())
                    days = int(match.group(1)) if match else 0

                    places.append({
                        'city': name.strip(),
                        'days': days,
                        'description': desc.strip(),
                        'coordinates': coords_text,
                        'lon': lon,
                        'lat': lat
                    })
    return places

def compute_travel_times_and_routes(places, ors_api_key, profile='driving-hgv'):
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
            route = client.directions(coords, profile=profile, format='geojson')
            duration_sec = route['features'][0]['properties']['segments'][0]['duration']
            travel_times.append(round(duration_sec / 3600, 2))
            routes_geojson.append(route['features'][0]['geometry'])
        except Exception as e:
            st.warning(f"Erreur ORS pour étape {i}: {e}")
            travel_times.append(0)
            routes_geojson.append(None)
    return travel_times, routes_geojson


st.set_page_config(page_title="RoadMap des babylove", page_icon="🌍")
st.title("📍 RoadMap des babylove")

st.markdown(f"**KML utilisé :** {KML_URL}")

if "places" not in st.session_state:
    st.session_state.places = []
if "travel_times" not in st.session_state:
    st.session_state.travel_times = []
if "routes_geojson" not in st.session_state:
    st.session_state.routes_geojson = []

if st.button("Calculer planning et afficher la carte"):

    with st.spinner("Chargement et parsing KML..."):
        st.session_state.places = parse_kml_from_url(KML_URL)

    if not st.session_state.places:
        st.warning("Aucune étape trouvée dans la couche 'Etapes du voyage'. Vérifie l'URL ou la structure KML.")
    else:
        with st.spinner("Calcul des durées de trajet..."):
            st.session_state.travel_times, st.session_state.routes_geojson = compute_travel_times_and_routes(
                st.session_state.places, ORS_API_KEY)

# Affichage du planning et carte seulement si on a les données
if st.session_state.places:
    places = st.session_state.places
    travel_times = st.session_state.travel_times
    routes_geojson = st.session_state.routes_geojson

    total_days = sum(p['days'] for p in places)
    total_travel_hours = sum(travel_times)

    st.subheader("🚍 Résumé de l'itinéraire")
    st.markdown(f"- Nombre d'étapes : **{len(places)}**")
    st.markdown(f"- 🛏️ Jours totaux sur place : **{total_days}** jours")
    st.markdown(
        f"- 🛣️ Temps total estimé de trajet : **{total_travel_hours:.2f} h** (~{total_travel_hours/24:.1f} jours)"
    )

    st.subheader("📆 Planning du voyage")
    for i, place in enumerate(places):
        st.markdown(f"🛏️ **Étape {i+1} : {place['city']}** - {place['days']} jours")
        if i < len(places)-1:
            st.markdown(f"→ 🚗 Trajet vers **{places[i+1]['city']}** : {travel_times[i+1]} heures")

    # Création carte folium
    if places[0]['lat'] and places[0]['lon']:
        m = folium.Map(location=[places[0]['lat'], places[0]['lon']], zoom_start=6)
    else:
        m = folium.Map(zoom_start=2)

    # Ajouter markers
    for p in places:
        if p['lat'] and p['lon']:
            folium.Marker(
                location=[p['lat'], p['lon']],
                popup=f"{p['city']}<br>{p['days']} jours",
                tooltip=p['city'],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

    # Ajouter les trajets
    for geojson in routes_geojson:
        if geojson:
            folium.GeoJson(geojson,
                           style_function=lambda x: {
                               'color': 'red', 'weight': 4, 'opacity': 0.7
                            }).add_to(m)

    st_folium(m, width=700, height=500)
