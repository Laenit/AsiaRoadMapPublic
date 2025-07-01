import streamlit as st
import requests
import xml.etree.ElementTree as ET
import re
from io import BytesIO


class KMLMixin:
    def strip_ns(self, tag):
        return tag.split('}')[-1]

    def get_place_from_kml_url(self, url, layer_name_keyword="etapes"):
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
            if self.strip_ns(folder.tag) == "Folder":
                folder_name = folder.findtext(
                    'kml:name', default='', namespaces=ns
                )
                folder_clean = folder_name.strip().lower()
                if layer_name_keyword in folder_clean:
                    for placemark in folder.findall(
                        './/kml:Placemark', namespaces=ns
                    ):
                        name = placemark.findtext(
                            'kml:name', default='(sans nom)', namespaces=ns
                        )
                        desc = placemark.findtext(
                            'kml:description', default='', namespaces=ns
                        )
                        coords_text = placemark.findtext(
                            './/kml:coordinates', default='', namespaces=ns
                        ).strip()
                        try:
                            lon, lat, *_ = map(float, coords_text.split(','))
                        except Exception:
                            lon = lat = None

                        match = re.search(
                            r"(\d+)\s*(j|jour|jours)", desc.lower()
                        )
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
