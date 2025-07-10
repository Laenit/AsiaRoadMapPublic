import openrouteservice


def compute_travel_time_and_route(
    from_place, to_place, ors_api_key, profile='driving-hgv'
):
    """
    Calcule le temps de trajet (en heures) et le GeoJSON de la route
    entre deux lieux avec OpenRouteService.

    Args:
        from_place (dict): Lieu de départ avec 'lat' et 'lon'.
        to_place (dict): Lieu d'arrivée avec 'lat' et 'lon'.
        ors_api_key (str): Clé API ORS.
        profile (str): Profil de trajet (par défaut: 'driving-hgv').

    Returns:
        tuple: (travel_time_hours, route_geojson)
            - travel_time_hours (float): Durée du trajet en heures.
            - route_geojson (dict): GeoJSON du trajet.
    """
    client = openrouteservice.Client(key=ors_api_key)

    if None in (from_place['lon'], from_place['lat'], to_place['lon'], to_place['lat']):
        # Coordonnées manquantes : renvoyer 0 et aucun GeoJSON
        return 0, None

    coords = [
        (from_place['lon'], from_place['lat']),
        (to_place['lon'], to_place['lat'])
    ]

    try:
        route = client.directions(
            coords, profile=profile, format='geojson'
        )
        duration_sec = route['features'][0]['properties']['segments'][0]['duration']
        travel_time_hours = round(duration_sec / 3600, 2)

        # Ajouter le temps au GeoJSON pour simplifier l’affichage
        route['features'][0]['properties']['custom_duration'] = travel_time_hours

        return travel_time_hours, route['features'][0]

    except Exception as e:
        # Log ou afficher l'erreur
        print(f"Erreur ORS entre {from_place['name']} et {to_place['name']}: {e}")
        return 0, None
