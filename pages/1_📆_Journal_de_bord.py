import streamlit as st
from utils.utils import format_duration_hm
from objects.trip import Trip
from objects.place import Place
from objects.day import Day
from objects.occupation import Occupation


# Journal de bord
st.subheader("📆 C'est quoi le plan ?")

trip = Trip()
trip.get_places_from_file()
trip.get_trip_from_place()
trip.get_travel_time_and_routes_from_file()


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
                                    occupation = Occupation(
                                        new_occupation,
                                        cost,
                                        type,
                                        place.name,
                                        day.name,
                                    )
                                    occupation.create_occupation()
                                    st.rerun()
                                if trip.data_file[place.name][day.name][type]:
                                    header_col = st.columns([3, 2, 0.5])
                                    header_col[0].markdown("**Nom**")
                                    header_col[1].markdown("**Montant (€)**")
                                    for occupation_name in (
                                        trip.data_file[place.name][day.name][type]
                                    ):
                                        occupation_data = day.get_occupation_information(
                                            type,
                                            occupation_name
                                        )
                                        occupation = Occupation(
                                            occupation_name,
                                            occupation_data["cost"],
                                            type,
                                            place.name,
                                            day.name,
                                        )
                                        cols = st.columns([3, 2, 0.5])
                                        with cols[0]:
                                            st.markdown(f"**{occupation.name}**")
                                        with cols[1]:
                                            st.markdown(
                                                f"{occupation.cost} €",
                                            )
                                        with cols[2]:
                                            with st.popover("⋮"):
                                                with st.popover(
                                                    "Éditer",
                                                ):
                                                    new_name = st.text_input(
                                                        label="Nom",
                                                        key=(
                                                            f"{place.name}_{day.name}"
                                                            f"_{type}_{occupation_name}_n"
                                                        )
                                                    )
                                                    new_price = st.number_input(
                                                        label="Prix (€)",
                                                        key=(
                                                            f"{place.name}_{day.name}"
                                                            f"_{type}_{occupation_name}_price"
                                                        )
                                                    )
                                                    if st.button(
                                                        "Enregistrer",
                                                        key=f"b_{place.name}{day.name}"
                                                        f"{type}{occupation.name}"
                                                    ):
                                                        if new_price != occupation.cost:
                                                            occupation.change_cost(new_price)
                                                        if new_name != occupation.name:
                                                            occupation.rename(new_name)
                                                        st.rerun()
                                                if st.button(
                                                    "🗑️ Supprimer",
                                                    key=f"del_{place.name}_{day.name}"
                                                    f"_{type}_{occupation.name}"
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
                                            type,
                                            occupation_name
                                        )
                                        cols = st.columns([3, 2])
                                        with cols[0]:
                                            st.markdown(f"**{occupation_name}**")
                                        with cols[1]:
                                            st.markdown(f"{occupation_data["cost"]} €")
            else:
                type = day_name
                with st.expander(type):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_occupation = st.text_input(
                            "Nom",
                            key=f"{place.name},{type},{occupation.name}txt",
                        )
                    with col2:
                        cost = st.number_input(
                            "Prix pour deux (€)",
                            key=f"{place.name},{type},{occupation.name}cost",
                        )
                    if st.button(
                        "Ajouter", key=f"{place.name},{type}"
                    ) and new_occupation:
                        occupation_add = Occupation(
                            new_occupation,
                            cost,
                            type,
                            place.name,
                            day=None,
                            general=True
                        )
                        occupation_add.create_occupation()
                        st.success(f"{occupation_add.name} ajouté(e) !")
                        st.rerun()
                    if trip.data_file[place.name][type]:
                        header_col = st.columns([1, 3, 2, 3, 1])
                        header_col[0].markdown("**✔️**")
                        header_col[1].markdown("**Nom**")
                        header_col[2].markdown("**Montant (€)**")
                        header_col[3].markdown("**Jour(s)**")
                        for occupation_name in trip.data_file[place.name][type]:
                            occupation_data = place.get_occupation_information(
                                type,
                                occupation_name
                            )
                            occupation = Occupation(
                                occupation_name,
                                occupation_data["cost"],
                                type,
                                place.name,
                                day=occupation_data["day"],
                                general=True
                            )
                            cols = st.columns([1, 3, 2, 3, 1])
                            with cols[0]:
                                st.checkbox(
                                    " ",
                                    key=f"{place.name}_{type}_{occupation.name}_{occupation.cost}",
                                    value=occupation.is_paid,
                                )
                            with cols[1]:
                                st.markdown(f"**{occupation.name}**")
                            with cols[2]:
                                st.markdown(f"{occupation.cost} €")
                            with cols[3]:
                                possibles_days = [
                                    j for j in place.get_information(place.path)
                                    if j.startswith("Jour")
                                ]
                                if type == "Activites":
                                    if occupation.day:
                                        index = int(occupation.day[-1])
                                    else:
                                        index = 0
                                    selected_day = st.selectbox(
                                        "Jour",
                                        [None] + possibles_days,
                                        key=f"{place.name}_{type}_{occupation.name}select",
                                        index=index,
                                        label_visibility="collapsed"
                                    )
                                    if selected_day != occupation.day:
                                        occupation.define_activity_days(selected_day)
                                        st.rerun()
                                if type == "Hebergements":
                                    if occupation.day:
                                        default = occupation.day
                                    else:
                                        default = []
                                    selected_days = st.multiselect(
                                        "Jours",
                                        possibles_days,
                                        key=f"{place.name}_{type}_{occupation.name}_select",
                                        default=default,
                                        label_visibility="collapsed",
                                    )
                                    if selected_days != occupation.day:
                                        occupation.define_housing_days(selected_days)
                                        st.rerun()
                            with cols[4]:
                                with st.popover("⋮"):
                                    with st.popover(
                                        "Éditer",
                                    ):
                                        new_name = st.text_input(
                                            label="Nom",
                                            key=(
                                                f"{place.name}_{day.name}"
                                                f"_{type}_{occupation_name}_n"
                                            )
                                        )
                                        new_price = st.number_input(
                                            label="Prix (€)",
                                            key=(
                                                f"{place.name}_{day.name}"
                                                f"_{type}_{occupation_name}_price"
                                            )
                                        )
                                        if st.button(
                                            "Enregistrer",
                                            key=f"b_{place.name}{day.name}"
                                            f"{type}{occupation.name}"
                                        ):
                                            if new_price != occupation.cost:
                                                occupation.change_cost(new_price)
                                            if new_name != occupation.name:
                                                occupation.rename(new_name)
                                            st.rerun()
                                    if st.button(
                                        "🗑️ Supprimer",
                                        key=f"del_{place.name}_{day.name}"
                                        f"_{type}_{occupation.name}"
                                    ):
                                        occupation.delete_occupation()
                                        st.rerun()

    if i < len(trip.places) - 1:
        day = Day(
            trip.places[i+1]["city"],
            1,
            None
        )

        if f"Trajet vers {trip.places[i+1]['city']}" not in day.get_type_information("Transports"):
            occupation_cost = 0
        else:
            occupation_cost = (
                day.get_occupation_information(
                    "Transports", f"Trajet vers {trip.places[i+1]['city']}"
                )["cost"]
            )
        occupation_trip = Occupation(
            f"Trajet vers {trip.places[i+1]['city']}",
            occupation_cost,
            "Transports",
            trip.places[i+1]["city"],
            "Jour 1",
        )
        occupation_trip.create_occupation()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"→ 🚍 Trajet vers **{occupation_trip.place}**"
                f" : {format_duration_hm(trip.travel_times[i])}"
            )
        with col2:
            new_price = st.number_input(
                label="Prix pour deux (€)",
                min_value=0,
                value=occupation_trip.cost,
                key=f"{occupation_trip.place}_transports"
            )
            if (
                new_price != occupation_trip.cost
            ):
                occupation_trip.change_cost(new_price)
                st.rerun()
