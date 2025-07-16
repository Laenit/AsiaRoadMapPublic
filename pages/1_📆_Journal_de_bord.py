import streamlit as st
from utils.utils import format_duration_hm
from objects.trip import Trip
from objects.place import Place
from objects.day import Day
from objects.occupation.generic_occupation import GenericOccupation


# Journal de bord
st.subheader("📆 C'est quoi le plan ?")

trip = Trip()
trip.get_places_from_file()
trip.get_trip_from_place()


# Ajout : On synchronise trip.places si nécessaire
if len(trip.places) != len(trip.data_file):
    trip.data_file = {p["city"]: {} for p in trip.places}

for i, (place_name, objects) in enumerate(trip.data_file.items()):
    place = Place(
        place_name,
        trip.places[i]["days"],
    )
    with st.expander(
        f"**Etape {i+1} - {place.name}** : {place.days_number} jour(s)"
    ):
        if st.button("Supprimer l'étape", key=f"{place.name}, sup"):
            place.delete_place()
            st.rerun()

        for j, (day_name, occupations) in enumerate(objects.items()):
            if day_name.startswith("Jour"):
                day = Day(
                    place.name,
                    j + 1,
                    trip.get_day_trip_number(place.name, j + 1),
                )
                with st.expander(f"📅 {day.name}"):
                    for type, items in occupations.items():
                        with st.expander(f"{type}"):
                            if type not in ["Activites", "Hebergements"]:
                                col1, col2 = st.columns(2)
                                with col1:
                                    new_occupation = st.text_input(
                                        "Nom", key=f"{place.name},{day.name},{type},txt"
                                    )
                                with col2:
                                    cost = st.number_input(
                                        "Prix pour deux (€)",
                                        key=f"{place.name},{day.name},{type},cost"
                                    )
                                if st.button(
                                    "Ajouter", key=f"{place.name},{day.name},{type}"
                                ) and new_occupation:
                                    occupation = GenericOccupation(
                                        new_occupation,
                                        cost,
                                        type,
                                        place.name,
                                        day.name,
                                    )
                                    occupation.create_occupation()
                                    st.rerun()
                                    st.success(f"{occupation.name} ajouté(e) !")
                                header_col = st.columns([3, 2, 2])
                                header_col[0].markdown("**Nom**")
                                header_col[1].markdown("**Montant (€)**")
                                header_col[2].markdown("**Supprimer**")
                                for occupation_name in (
                                    trip.data_file[place.name][day.name][type]
                                ):
                                    occupation_data = day.get_occupation_information(
                                        occupation_name
                                    )
                                    occupation = GenericOccupation(
                                        occupation_name,
                                        occupation_data["cost"],
                                        type,
                                        place.name,
                                        day.name,
                                    )
                                    cols = st.columns([3, 2, 2])
                                    with cols[0]:
                                        col_name = st.columns([1.5, 1])
                                        with col_name[1]:
                                            is_on = st.toggle(
                                                label="Editer",
                                                key=f"{place.name}_{day.name}_{type}_toggle",
                                                value=False,
                                            )
                                        with col_name[0]:
                                            if is_on:
                                                new_name = st.text_input(
                                                    label=" ",
                                                    value=occupation.name,
                                                    label_visibility="collapsed"
                                                )
                                            if new_name != occupation.name:
                                                occupation.rename(new_name)
                                                st.rerun()
                                            else:
                                                st.markdown(f"**{occupation.name}**")
                                    with cols[1]:
                                        new_price = st.number_input(
                                            label=" ",
                                            value=occupation.cost,
                                            label_visibility="collapsed",
                                            key=f"{place.name}_{day.name}_{type}_price"
                                        )
                                        if (
                                            new_price != occupation.cost
                                        ):
                                            occupation.change_cost(new_price)
                                            st.rerun()
                                    with cols[2]:
                                        if st.button(
                                            "🗑️",
                                            key=f"{place.name}_{day.name}_{type}_delete",
                                        ):
                                            occupation.delete_occupation()
                                            st.rerun()
                            else:
                                if trip.data_file[place.name][day.name][type]:
                                    header_col = st.columns([3, 2])
                                    header_col[0].markdown("**Nom**")
                                    header_col[1].markdown("**Montant (€)**")
                                    for occupation_name in (
                                        trip.data_file[place.name][day.name][type]
                                    ):
                                        occupation_data = day.get_occupation_information(
                                            occupation_name
                                        )
                                        cols = st.columns([3, 2])
                                        with cols[0]:
                                            st.markdown(f"**{occupation_name}**")
                                        with cols[1]:
                                            st.markdown(f"{occupation_data["cost"]} €")
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
                            trip.data_file[place][cat][new_activity] = [cost, "0"]
                        if cat == "Hebergements":
                            trip.data_file[place][cat][new_activity] = [cost, []]
                        save_data(trip.data_file, DATA_FILE)
                        st.success(f"{new_activity} ajouté(e) !")
                    if trip.data_file[place][cat]:
                        header_col = st.columns([1, 3, 2, 3, 2])
                        header_col[0].markdown("**✔️**")
                        header_col[1].markdown("**Nom**")
                        header_col[2].markdown("**Montant (€)**")
                        header_col[3].markdown("**Jour(s)**")
                        header_col[4].markdown("**Supprimer**")
                        for name, cost_jour in trip.data_file[place][cat].items():
                            cols = st.columns([1, 3, 2, 3, 2])
                            with cols[0]:
                                st.checkbox(
                                    " ",
                                    key=f"{place}_{cat}_{name}",
                                )
                            with cols[1]:
                                col_name = st.columns([1, 1.5])
                                with col_name[1]:
                                    is_on = st.toggle(
                                        label="Editer",
                                        key=f"{place}_{cat}_toggle",
                                        value=False,
                                    )
                                with col_name[0]:
                                    if is_on:
                                        new_name = st.text_input(
                                            label=" ",
                                            value=name,
                                            label_visibility="collapsed"
                                        )
                                        if new_name != name:
                                            del trip.data_file[place][cat][name]
                                            trip.data_file[place][cat][new_name] = cost_jour
                                            if cat == "Activites":
                                                del trip.data_file[place][
                                                    "Jours"
                                                ][cost_jour[1]][name]
                                                trip.data_file[place][
                                                    "Jours"
                                                ][cost_jour[1]][cat][new_name] = cost_jour[0]
                                            else:
                                                for jour in cost_jour[1]:
                                                    del trip.data_file[place][
                                                        "Jours"
                                                    ][jour][cat][name]
                                                    trip.data_file[place][
                                                        "Jours"
                                                    ][jour][cat][new_name] = cost_jour[0]
                                            save_data(trip.data_file, DATA_FILE)
                                            st.rerun()
                                    else:
                                        st.markdown(f"**{name}**")
                            with cols[2]:
                                new_price = st.number_input(
                                    label=" ",
                                    value=cost_jour[0],
                                    label_visibility="collapsed",
                                    key=f"{place}_{cat}_price"
                                )
                                if (
                                    new_price != (
                                        trip.data_file[place][cat][name][0]
                                    )
                                ):
                                    trip.data_file[place][cat][name] = [
                                        new_price, cost_jour[1]
                                    ]
                                    save_data(trip.data_file, DATA_FILE)
                                    st.rerun()
                            with cols[3]:
                                jours_possibles = [
                                    j for j in trip.data_file[place]["Jours"].keys()
                                    if j.startswith("Jour")
                                ]
                                if cat == "Activites":
                                    jour_select = st.selectbox(
                                        "Jour",
                                        ["0"] + jours_possibles,
                                        key=f"{place}_{cat}_select",
                                        index=int(trip.data_file[place][cat][name][1][-1]),
                                        label_visibility="collapsed"
                                    )
                                    previous_day = trip.data_file[place][cat][name][1]
                                    if (
                                        jour_select != "0" and
                                        name not in (
                                            list(
                                                trip.data_file[place]["Jours"][jour_select][
                                                    cat
                                                ].keys()
                                            )
                                        )
                                    ):
                                        trip.data_file[place]["Jours"][jour_select][cat][name] = (
                                            cost_jour[0]
                                        )
                                        trip.data_file[place][cat][name] = [
                                            cost_jour[0],
                                            jour_select,
                                        ]
                                        save_data(trip.data_file, DATA_FILE)
                                        st.rerun()
                                    if previous_day != "0" and previous_day != jour_select:
                                        del (
                                            trip.data_file[place]["Jours"][previous_day][cat][
                                                name
                                            ]
                                        )
                                        trip.data_file[place][cat][name] = [
                                            cost_jour[0],
                                            jour_select,
                                        ]
                                        save_data(trip.data_file, DATA_FILE)
                                        st.rerun()
                                if cat == "Hebergements":
                                    jours_select = st.multiselect(
                                        "Jours",
                                        jours_possibles,
                                        key=f"{place}_{cat}_select",
                                        default=trip.data_file[place][cat][name][1],
                                        label_visibility="collapsed",
                                    )
                                    previous_days = trip.data_file[place][cat][name][1]
                                    for jour_select in jours_select:
                                        if (
                                            name not in (
                                                list(
                                                    trip.data_file[place]["Jours"][jour_select][
                                                        cat
                                                    ].keys()
                                                )
                                            )
                                        ):
                                            trip.data_file[place]["Jours"][jour_select][cat][
                                                name
                                            ] = (
                                                cost_jour[0]
                                            )
                                            trip.data_file[place][cat][name][1].append(jour_select)
                                            save_data(trip.data_file, DATA_FILE)
                                            st.rerun()
                                    for previous_day in previous_days:
                                        if previous_day not in jours_select:
                                            del trip.data_file[place]["Jours"][previous_day][cat][
                                                name
                                            ]
                                            trip.data_file[place][cat][name][1].remove(previous_day)
                                            save_data(trip.data_file, DATA_FILE)
                                            st.rerun()
                            with cols[4]:
                                if st.button(
                                    "🗑️",
                                    key=f"d_{place}_{cat}_{name}",
                                ):
                                    suppression_cat.append((place, cat, name))

    if i < len(trip.places) - 1:
        if (
            f"Trajet vers {trip.places[i+1]['city']}"
            not in trip.data_file[trip.places[i+1]["city"]]["Jours"]["Jour 1"]["Transports"].keys()
        ):
            trip.data_file[trip.places[i+1]["city"]]["Jours"]["Jour 1"]["Transports"][
                            f"Trajet vers {trip.places[i+1]['city']}"
                        ] = 0
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"→ 🚍 Trajet vers **{trip.places[i+1]['city']}**"
                f" : {format_duration_hm(travel_times[i])}"
            )
        with col2:
            new_price = st.number_input(
                label="Prix pour deux (€)",
                min_value=0,
                value=(
                    trip.data_file[trip.places[i+1]["city"]]["Jours"]["Jour 1"]["Transports"][
                        f"Trajet vers {trip.places[i+1]['city']}"
                    ]
                ),
                key=f"{trip.places[i+1]['city']}_transports"
            )
            if (
                new_price != trip.data_file[trip.places[i+1]["city"]]["Jours"]["Jour 1"]["Transports"][
                        f"Trajet vers {trip.places[i+1]['city']}"
                    ]
            ):
                trip.data_file[trip.places[i+1]["city"]]["Jours"]["Jour 1"]["Transports"][
                        f"Trajet vers {trip.places[i+1]['city']}"
                    ] = new_price
                save_data(trip.data_file, DATA_FILE)
                st.rerun()

# Suppression des étapes entières
if suppression_etape:
    for index in sorted(suppression_etape, reverse=True):
        place_name = trip.places[index]["city"]
        # Supprime de data_file
        if place_name in trip.data_file:
            del trip.data_file[place_name]
        # Supprime de trip.places et travel_times dans route_data
        del trip.places[index]
        if index > 0:
            del travel_times[index - 1]
        else:
            del travel_times[0]
    # Sauvegarde
    save_data(trip.data_file, DATA_FILE)
    save_data({"trip.places": trip.places, "travel_times": travel_times}, ROUTE_FILE)
    st.success("✅ Étape supprimée avec succès !")
    st.rerun()

# Suppression des grandes actis
if suppression_cat:
    for place, cat, name in suppression_cat:
        if cat == "Activites":
            try:
                jour_select = trip.data_file[place][cat][name][1]
                del trip.data_file[place][cat][name]
                if jour_select != "0":
                    del trip.data_file[place]["Jours"][jour_select][cat][name]
            except IndexError:
                pass
        if cat == "Hebergements":
            try:
                jours_select = trip.data_file[place][cat][name][1]
                del trip.data_file[place][cat][name]
                for jour_select in jours_select:
                    del trip.data_file[place]["Jours"][jour_select][cat][name]
            except IndexError:
                pass
    save_data(trip.data_file, DATA_FILE)
    st.success("✅ Élément(s) supprimé(s) avec succès !")
    st.rerun()

# Suppression d’activités individuelles
if suppression:
    for place, jour, act, name in suppression:
        try:
            del trip.data_file[place]["Jours"][jour][act][name]
        except IndexError:
            pass
    save_data(trip.data_file, DATA_FILE)
    st.success("✅ Élément(s) supprimé(s) avec succès !")
    st.rerun()
