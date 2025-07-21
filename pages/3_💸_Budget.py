import streamlit as st
import plotly.express as px
from objects.trip import Trip
from objects.costs import Costs

trip = Trip()
trip.get_places_from_file()
trip.get_trip_from_place()
trip.get_travel_time_and_routes_from_file()

costs = Costs()


# --- Interface Streamlit
st.title("💰 Gestion du budget du voyage")

# --- Formulaire ajout/modification dépense admin
st.header("🗂️ Gestion des dépenses administratives")
with st.form("admin_form"):
    name = st.text_input("Nom de la dépense")
    price = st.number_input("Montant pour une personne (€)", format="%.2f")
    buyer = st.selectbox(
        "Pour qui ?",
        [
            "Les deux",
            "Marie",
            "Tinaël"
        ]
    )
    type = st.selectbox(
        "Type de dépense",
        [
            "Equipement",
            "Administratif",
            "Souvenir",
            "Santé"
        ]
    )
    submitted = st.form_submit_button("Enregistrer")
    if submitted:
        if name.strip() == "":
            st.error("Le nom ne peut pas être vide")
        else:
            costs.create_cost(
                name,
                price,
                buyer,
                type
            )
            st.success(
                "Dépense administrative ajoutée !"
            )
            st.rerun()


if costs.data_file:
    # En-têtes
    header_cols = st.columns([3, 3, 3, 3, 3])
    header_cols[0].markdown("**Nom**")
    header_cols[1].markdown("**Montant (€)**")
    header_cols[2].markdown("**Catégorie**")
    header_cols[3].markdown("**Pour qui ?**")
    header_cols[4].markdown("**Supprimer**")

    for name, data in costs.data_file.items():
        cols = st.columns([3, 3, 3, 3, 3])
        cols[0].write(name)
        cols[1].write(f"{data["cost"]:.2f}")
        cols[2].write(f"{data["category"]}")
        cols[3].write(f"{data["buyer"]}")
        if cols[4].button("🗑️", key=f"delete_{name}"):
            costs.delete_cost(name)
            st.success("Dépense administrative supprimée !")
            st.rerun()

# --- Calcul dépenses par ville
place_dataframe = trip.get_places_dataframe()
cost_dataframe = costs.get_costs_dataframe()

# --- Totaux
total_villes = place_dataframe["cost"].sum()
total_marie = cost_dataframe["Marie_cost"].sum()
total_tinael = cost_dataframe["Tinael_cost"].sum()
total_marie_global = total_villes/2 + total_marie
total_tinael_global = total_villes/2 + total_tinael

st.header(f"💸 Dépenses totales Marie : {total_marie_global:.2f} €")
st.header(f"💸 Dépenses totales Tinaël : {total_tinael_global:.2f} €")


# --- Tableau résumé par ville + admin
st.subheader("📋 Récapitulatif des dépenses par ville")
st.table(place_dataframe)

days_dataframe = trip.get_trip_days_dataframe()

# Camembert
# Calcul des totaux par catégorie (hors admin)
types = ["Activites", "Repas", "Transports", "Hebergements"]
costs_type = []
for type in types:
    costs_type.append(trip.get_trip_type_cost(type)/2)

categories = ["Equipement", "Administratif", "Souvenir", "Santé"]
costs_category_marie = []
costs_category_tinael = []
for category in categories:
    costs_category_marie.append(
        cost_dataframe[cost_dataframe["category"] == category]["Marie_cost"].sum()
    )
    costs_category_tinael.append(
        cost_dataframe[cost_dataframe["category"] == category]["Tinael_cost"].sum()
    )

# Préparer données pour camembert
labels_cat = types + categories
costs_repartition_marie = costs_type + costs_category_marie
costs_repartition_tinael = costs_type + costs_category_tinael

fig_cat_marie = px.pie(
    names=labels_cat,
    values=costs_repartition_marie,
    title="Répartition des dépenses de Marie",
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
fig_cat_tinael = px.pie(
    names=labels_cat,
    values=costs_repartition_tinael,
    title="Répartition des dépenses de Tinaël",
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

cols = st.columns([1, 1])
with cols[0]:
    st.plotly_chart(fig_cat_marie, use_container_width=True)
with cols[1]:
    st.plotly_chart(fig_cat_tinael, use_container_width=True)

# --- Graphique d'évolution du budget jour par jour (hors admin)


# Données pour graphique
total_days = sum(place["days"] for place in trip.places)

days = [f"Jour {i+1}" for i in range(total_days)]
costs = [days_dataframe.iloc[i]["cost"] for i in range(total_days)]


# Tracer le graphique en courbe
fig_jours = px.line(
    x=days,
    y=costs,
    markers=True,
    labels={"x": "Jour", "y": "Dépenses (€)"},
    title="Évolution des dépenses par jour",
)

st.plotly_chart(fig_jours, use_container_width=True)
