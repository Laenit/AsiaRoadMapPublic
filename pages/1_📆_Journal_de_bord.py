import streamlit as st
from data.json_utils import load_data, save_data
from utils import format_duration_hm
from trip import Trip

DATA_FILE = "trip.json"
ROUTE_FILE = "route.json"

# Journal de bord
st.subheader("📆 C'est quoi le plan ?")

route_data = load_data(ROUTE_FILE)
places = route_data["places"]
travel_times = route_data["travel_times"]
data = load_data(DATA_FILE)
trip = Trip(places, data)
trip.get_trip_from_place()

# Ajout : On synchronise places si nécessaire
if len(places) != len(trip.trip_data):
    trip.trip_data = {p["city"]: {} for p in places}

suppression = []
suppression_etape = []
suppression_cat = []

for i, (place, cats) in enumerate(trip.trip_data.items()):
    with st.expander(
        f"**Etape {i+1} - {place}** : {places[i]['days']} jour(s)"
    ):
        if st.button("Supprimer l'étape", key=f"{place}, sup"):
            suppression_etape.append(i)  # On stocke l’index et pas le nom

        for cat, jours in cats.items():
            if cat == "Jours":
                for jour, activities in jours.items():
                    with st.expander(f"📅 {jour}"):
                        for activity, items in activities.items():
                            with st.expander(f"{activity}"):
                                if activity not in ["Activites", "Hebergements"]:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        new_activity = st.text_input(
                                            "Nom", key=f"{place},{jour},{activity},txt"
                                        )
                                    with col2:
                                        cost = st.number_input(
                                            "Prix pour deux (€)",
                                            key=f"{place},{jour},{activity},cost"
                                        )
                                    if st.button(
                                        "Ajouter", key=f"{place},{jour},{activity}"
                                    ) and new_activity:
                                        trip.trip_data[place][cat][jour][activity][new_activity] = (
                                            cost
                                        )
                                        save_data(trip.trip_data, DATA_FILE)
                                        st.rerun()
                                        st.success(f"{new_activity} ajouté(e) !")
                                    if trip.trip_data[place][cat][jour][activity]:
                                        header_col = st.columns([3, 2, 2])
                                        header_col[0].markdown("**Nom**")
                                        header_col[1].markdown("**Montant (€)**")
                                        header_col[2].markdown("**Supprimer**")
                                        for name in (
                                            trip.trip_data[place][cat][jour][activity]
                                        ):
                                            cost_val = (
                                                trip.trip_data[place][cat][jour][activity][name]
                                            )
                                            cols = st.columns([3, 2, 2])
                                            with cols[0]:
                                                st.markdown(f"**{name}**")
                                            with cols[1]:
                                                st.markdown(f"{cost_val} €")
                                            with cols[2]:
                                                if st.button(
                                                    "🗑️",
                                                    key=f"d_{place}_{jour}_{activity}_{name}",
                                                ):
                                                    suppression.append(
                                                        (place, jour, activity, name)
                                                    )
                                else:
                                    if trip.trip_data[place][cat][jour][activity]:
                                        header_col = st.columns([3, 2])
                                        header_col[0].markdown("**Nom**")
                                        header_col[1].markdown("**Montant (€)**")
                                        for name, cost_val in (
                                            trip.trip_data[place][cat][jour][activity].items()
                                        ):
                                            cols = st.columns([3, 2])
                                            with cols[0]:
                                                st.markdown(f"**{name}**")
                                            with cols[1]:
                                                st.markdown(f"{cost_val} €")

            else:
                with st.expander(f"{cat}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_activity = st.text_input(
                            "Nom", key=f"{place},{cat},txt"
                        )
                    with col2:
                        cost = st.number_input(
                            "Prix pour deux (€)", key=f"{place},{cat},cost"
                        )
                    if st.button(
                        "Ajouter", key=f"{place},{cat}"
                    ) and new_activity:
                        if cat == "Activites":
                            trip.trip_data[place][cat][new_activity] = [cost, "0"]
                        if cat == "Hebergements":
                            trip.trip_data[place][cat][new_activity] = [cost, []]
                        save_data(trip.trip_data, DATA_FILE)
                        st.success(f"{new_activity} ajouté(e) !")
                    if trip.trip_data[place][cat]:
                        header_col = st.columns([1, 3, 2, 3, 2])
                        header_col[0].markdown("**✔️**")
                        header_col[1].markdown("**Nom**")
                        header_col[2].markdown("**Montant (€)**")
                        header_col[3].markdown("**Jour(s)**")
                        header_col[4].markdown("**Supprimer**")
                        for name, cost_jour in trip.trip_data[place][cat].items():
                            cols = st.columns([1, 3, 2, 3, 2])
                            with cols[0]:
                                st.checkbox(
                                    " ",
                                    key=f"{place}_{cat}_{name}",
                                )
                            with cols[1]:
                                st.markdown(f"**{name}**")
                            with cols[2]:
                                st.markdown(f"{cost_jour[0]} €")
                            with cols[3]:
                                jours_possibles = [
                                    j for j in trip.trip_data[place]["Jours"].keys()
                                    if j.startswith("Jour")
                                ]
                                if cat == "Activites":
                                    jour_select = st.selectbox(
                                        "Jour",
                                        ["0"] + jours_possibles,
                                        key=f"{place}_{cat}_select",
                                        index=int(trip.trip_data[place][cat][name][1][-1]),
                                        label_visibility="collapsed"
                                    )
                                    previous_day = trip.trip_data[place][cat][name][1]
                                    if (
                                        jour_select != "0" and
                                        name not in (
                                            list(
                                                trip.trip_data[place]["Jours"][jour_select][
                                                    cat
                                                ].keys()
                                            )
                                        )
                                    ):
                                        trip.trip_data[place]["Jours"][jour_select][cat][name] = (
                                            cost
                                        )
                                        trip.trip_data[place][cat][name] = [
                                            cost,
                                            jour_select,
                                        ]
                                        save_data(trip.trip_data, DATA_FILE)
                                        st.rerun()
                                    if previous_day != "0" and previous_day != jour_select:
                                        del (
                                            trip.trip_data[place]["Jours"][previous_day][cat][
                                                name
                                            ]
                                        )
                                        trip.trip_data[place][cat][name] = [
                                            cost,
                                            jour_select,
                                        ]
                                        save_data(trip.trip_data, DATA_FILE)
                                        st.rerun()
                                if cat == "Hebergements":
                                    jours_select = st.multiselect(
                                        "Jours",
                                        jours_possibles,
                                        key=f"{place}_{cat}_select",
                                        default=trip.trip_data[place][cat][name][1],
                                        label_visibility="collapsed",
                                    )
                                    previous_days = trip.trip_data[place][cat][name][1]
                                    for jour_select in jours_select:
                                        if (
                                            name not in (
                                                list(
                                                    trip.trip_data[place]["Jours"][jour_select][
                                                        cat
                                                    ].keys()
                                                )
                                            )
                                        ):
                                            trip.trip_data[place]["Jours"][jour_select][cat][
                                                name
                                            ] = (
                                                cost
                                            )
                                            trip.trip_data[place][cat][name][1].append(jour_select)
                                            save_data(trip.trip_data, DATA_FILE)
                                            st.rerun()
                                    for previous_day in previous_days:
                                        if previous_day not in jours_select:
                                            del trip.trip_data[place]["Jours"][previous_day][cat][
                                                name
                                            ]
                                            trip.trip_data[place][cat][name][1].remove(previous_day)
                                            save_data(trip.trip_data, DATA_FILE)
                                            st.rerun()
                            with cols[4]:
                                if st.button(
                                    "🗑️",
                                    key=f"d_{place}_{cat}_{name}",
                                ):
                                    suppression_cat.append((place, cat, name))

    if i < len(places) - 1:
        st.markdown(
            f"→ 🚍 Trajet vers **{places[i+1]['city']}**"
            f" : {format_duration_hm(travel_times[i])}"
        )

# Suppression des étapes entières
if suppression_etape:
    for index in sorted(suppression_etape, reverse=True):
        place_name = places[index]["city"]
        # Supprime de trip_data
        if place_name in trip.trip_data:
            del trip.trip_data[place_name]
        # Supprime de places et travel_times dans route_data
        del places[index]
        if index > 0:
            del travel_times[index - 1]
        else:
            del travel_times[0]
    # Sauvegarde
    save_data(trip.trip_data, DATA_FILE)
    save_data({"places": places, "travel_times": travel_times}, ROUTE_FILE)
    st.success("✅ Étape supprimée avec succès !")
    st.rerun()

# Suppression des grandes acits
if suppression_cat:
    for place, cat, name in suppression_cat:
        if cat == "Activite":
            try:
                jour_select = trip.trip_data[place][cat][name][1]
                del trip.trip_data[place][cat][name]
                if jour_select != "Jour 0":
                    del trip.trip_data[place]["Jours"][jour_select][cat][name]
            except IndexError:
                pass
        if cat == "Hebergements":
            try:
                jours_select = trip.trip_data[place][cat][name][1]
                del trip.trip_data[place][cat][name]
                for jour_select in jours_select:
                    del trip.trip_data[place]["Jours"][jour_select][cat][name]
            except IndexError:
                pass
    save_data(trip.trip_data, DATA_FILE)
    st.success("✅ Élément(s) supprimé(s) avec succès !")
    st.rerun()

# Suppression d’activités individuelles
if suppression:
    for place, jour, act, name in suppression:
        try:
            del trip.trip_data[place][jour][act][name]
        except IndexError:
            pass
    save_data(trip.trip_data, DATA_FILE)
    st.success("✅ Élément(s) supprimé(s) avec succès !")
    st.rerun()
