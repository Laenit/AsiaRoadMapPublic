def get_trip_from_place(places):
    trip = {}
    for place in places:
        days = {}
        for i in range(place["days"]):
            days[f"Jour {i+1}"] = {
                "Activités": [],
                "Repas": [],
                "Transports": [],
            }
        trip[
            f"{
                f"{place['city']}"
            }"
        ] = days
    return trip
