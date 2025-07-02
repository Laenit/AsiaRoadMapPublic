import streamlit as st
from data.json_utils import load_data, save_data
from utils import format_duration_hm
from trip import Trip
from Welcome_to_Asia import places, travel_times

DATA_FILE = "trip.json"

# Journal de bord
st.subheader("📆 C'est quoi le plan ?")

data = load_data(DATA_FILE)
trip = Trip(places, data)
trip.get_trip_from_place()
save_data(trip.trip_data, DATA_FILE)

suppression = []

for i, (place, jours) in enumerate(trip.trip_data.items()):
    with st.expander(
        f"**Etape {i+1} - {place}** : {places[i]['days']} jour(s)"
    ):
        for jour, activities in jours.items():
            with st.expander(f"📅 {jour}"):
                for activity, items in activities.items():
                    with st.expander(f"{activity}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_activity = st.text_input(
                                "Nom", key=f"{place},{jour},{activity},txt"
                            )
                        with col2:
                            cost = st.text_input(
                                "Prix ($)", key=f"{place},{jour},{activity},cost"
                            )
                        if st.button(
                            "Ajouter", key=f"{place},{jour},{activity}"
                        ) and new_activity:
                            trip.trip_data[place][jour][activity].append(
                                {
                                    new_activity: int(cost) if cost.isdigit()
                                    else 0
                                }
                            )
                            save_data(trip.trip_data, DATA_FILE)
                            st.success(f"{new_activity} ajouté(e) !")
                        if trip.trip_data[place][jour][activity]:
                            header_col = st.columns([1, 3, 2, 2])
                            header_col[0].markdown("**✔️**")
                            header_col[1].markdown("**Nom**")
                            header_col[2].markdown("**Montant (€)**")
                            header_col[3].markdown("**Supprimer**")
                            for idx, item in enumerate(
                                trip.trip_data[place][jour][activity]
                            ):
                                name, cost_val = list(item.items())[0]
                                cols = st.columns([1, 3, 2, 2])
                                with cols[0]:
                                    st.checkbox(
                                        "",
                                        key=f"{place}_{jour}_{activity}_{name}_{idx}",
                                    )
                                with cols[1]:
                                    st.markdown(f"**{name}**")
                                with cols[2]:
                                    st.markdown(f"{cost_val} $")
                                with cols[3]:
                                    if st.button(
                                        "🗑️",
                                        key=f"d_{place}_{jour}_{activity}_{name}_{idx}",
                                    ):
                                        suppression.append((place, jour, activity, idx))

    if i < len(places) - 1:
        st.markdown(
            f"→ 🚍 Trajet vers **{places[i+1]['city']}**"
            f" : {format_duration_hm(travel_times[i])}"
        )

if suppression:
    for place, jour, act, index in suppression:
        try:
            del trip.trip_data[place][jour][act][index]
        except IndexError:
            pass
    save_data(trip.trip_data, DATA_FILE)
    st.success("✅ Élément(s) supprimé(s) avec succès !")
    st.rerun()
