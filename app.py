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
                    coords_text = placemark.findtext('.//kml:coordinates', default='', namespaces=ns).strip()
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


def format_duration_hm(hours):
    h = int(hours)
    m = int(round((hours - h) * 60))
    return f"{h}h{m:02d}"


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
            route['features'][0]['properties']['custom_duration'] = round(duration_sec / 3600, 2)
            routes_geojson.append(route['features'][0])
        except Exception as e:
            st.warning(f"Erreur ORS pour étape {i}: {e}")
            travel_times.append(0)
            routes_geojson.append(None)
    return travel_times, routes_geojson


# --- STREAMLIT UI ---
st.set_page_config(page_title="RoadMap des babylove", page_icon="🌍")
st.title("📍 RoadMap des babylove")

if st.button("🔁 Mettre à jour l'itinéraire"):

    with st.spinner("📥 Chargement et parsing du KML..."):
        st.session_state.places = parse_kml_from_url(KML_URL)

    if not st.session_state.places:
        st.warning("Aucune étape trouvée dans la couche 'Etapes du voyage'. Vérifie l'URL ou la structure KML.")
    else:
        with st.spinner("🧮 Calcul des durées de trajet..."):
            st.session_state.travel_times, st.session_state.routes_geojson = compute_travel_times_and_routes(
                st.session_state.places, ORS_API_KEY)

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
    st.markdown(f"- 🛣️ Temps total estimé de trajet : **{format_duration_hm(total_travel_hours)}** (~{total_travel_hours/24:.1f} jours)")

    st.subheader("📆 C'est quoi le plan ?")
    for i, place in enumerate(places):
        st.markdown(f"🛏️ **Étape {i+1} : {place['city']}** - {place['days']} jours")
        if i < len(places)-1:
            st.markdown(f"→ 🚍 Trajet vers **{places[i+1]['city']}** : {format_duration_hm(travel_times[i+1])}")

    # --- FOLIUM MAP ---
    if places[0]['lat'] and places[0]['lon']:
        m = folium.Map(location=[places[0]['lat'], places[0]['lon']], zoom_start=6)
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
                style_function=lambda x: {'color': 'red', 'weight': 4, 'opacity': 0.7},
                tooltip=f"⏱️ {format_duration_hm(duration)} de trajet"
            ).add_to(m)

    st.subheader("🗺️ C'est où qu'elles sont les étapes ?")
    st_folium(m, width=700, height=500)
