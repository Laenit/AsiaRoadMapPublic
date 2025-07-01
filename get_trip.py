def get_trip_from_place(places):
    trip = {}
    for j, place in enumerate(places):
        days = {}
        for i in range(place["days"]):
            days[f"Jour {i+1}"] = [i]
        trip[
            f"{
                f"🛏️ **Étape {j+1} : {place['city']}** - {place['days']} jours"
            }"
        ] = days
    return trip
