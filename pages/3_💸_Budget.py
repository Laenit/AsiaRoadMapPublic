import streamlit as st
import plotly.express as px
import pandas as pd
from data.json_utils import load_data, save_data

# --- Fichiers de données
TRIP_FILE = "trip.json"
ADMIN_FILE = "admin_costs.json"


# --- Calcul total par ville (somme Activites+Repas+Transports)
def calc_costs_per_ville(data):
    result = {}
    for ville, jours in data.items():
        total = 0
        for _, details in jours.items():
            for cat in ["Activites", "Repas", "Transports"]:
                for elt in details.get(cat, []):
                    total += list(elt.values())[0]
        result[ville] = total
    return result


# --- Calcul des coûts totaux par catégorie (hors admin)
def calc_costs_villes(data):
    total = {"Activites": 0, "Repas": 0, "Transports": 0}
    for _, jours in data.items():
        for _, details in jours.items():
            for cat in total.keys():
                for elt in details.get(cat, []):
                    total[cat] += list(elt.values())[0]
    return total


# --- Calcul budget jour par jour (villes + admin)
def calc_budget_jour(data, admin_costs):
    budget_jour = {}
    for _, jours in data.items():
        for jour, details in jours.items():
            total = 0
            for cat in ["Activites", "Repas", "Transports"]:
                for elt in details.get(cat, []):
                    total += list(elt.values())[0]
            budget_jour[jour] = budget_jour.get(jour, 0) + total

    # Ajouter admin à chaque jour concerné
    for jour, montant in admin_costs.items():
        budget_jour[jour] = budget_jour.get(jour, 0) + montant

    # Tri chronologique par numéro de jour (ex: "Jour 1", "Jour 2", ...)
    sorted_budget = sorted(budget_jour.items(), key=lambda x: int(x[0].split()[1]))
    return sorted_budget


# --- Interface Streamlit
st.title("💰 Gestion du budget du voyage")

voyage_data = load_data(TRIP_FILE)
admin_costs = load_data(ADMIN_FILE)

# --- Formulaire ajout/modification dépense admin
st.header("🗂️ Gestion des dépenses administratives")
with st.form("admin_form"):
    nom = st.text_input("Nom de la dépense administrative")
    montant = st.number_input("Montant (€)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Enregistrer")
    if submitted:
        if nom.strip() == "":
            st.error("Le nom ne peut pas être vide")
        else:
            admin_costs[nom] = admin_costs.get(nom, 0) + montant
            save_data(admin_costs, ADMIN_FILE)
            st.success(
                f"Dépense administrative ajoutée/modifiée :"
                f"{nom} = {admin_costs[nom]:.2f} €"
            )
            st.rerun()


if admin_costs:
    # En-têtes
    header_cols = st.columns([0.1, 0.3, 0.3, 0.3])
    header_cols[0].markdown("**✔️**")
    header_cols[1].markdown("**Nom**")
    header_cols[2].markdown("**Montant (€)**")
    header_cols[3].markdown("**Supprimer**")

    for nom, montant in admin_costs.items():
        cols = st.columns([0.1, 0.3, 0.3, 0.3])
        cols[0].checkbox(
            "", value=False, label_visibility="collapsed", key=f"visu_check_{nom}"
        )
        cols[1].write(nom)
        cols[2].write(f"{montant:.2f}")
        if cols[3].button("🗑️", key=f"delete_{nom}"):
            del admin_costs[nom]
            save_data(admin_costs, ADMIN_FILE)
            st.success(f"Dépense administrative supprimée : {nom}")
            st.rerun()
else:
    st.info("Aucune dépense administrative enregistrée.")

# --- Calcul dépenses par ville
depenses_villes = calc_costs_per_ville(voyage_data)

# --- Totaux
total_villes = sum(depenses_villes.values())
total_admin = sum(admin_costs.values())
total_global = total_villes + total_admin

st.header(f"💸 Dépenses totales : {total_global:.2f} €")


# --- Tableau résumé par ville + admin
# Préparer dataframe
depense_label = "Dépenses villes ($)"
df = pd.DataFrame.from_dict(
    depenses_villes, orient='index', columns=[depense_label]
)
df.index.name = "Ville"
df.reset_index(inplace=True)

# Ajouter ligne admin (somme de toutes dépenses admin sous une seule ligne)
df_admin = pd.DataFrame(
    [["Administratif", total_admin]], columns=["Ville", depense_label]
)
df = pd.concat([df, df_admin], ignore_index=True)

# Ajouter ligne total général
df_total = pd.DataFrame([["TOTAL", total_global]], columns=["Ville", depense_label])
df = pd.concat([df, df_total], ignore_index=True)

st.subheader("📋 Récapitulatif des dépenses")
st.table(df)

# Camembert
# Calcul des totaux par catégorie (hors admin)
totaux_cat = calc_costs_villes(voyage_data)

# Ajouter les coûts admin dans la catégorie 'Administratif'
totaux_cat["Administratif"] = total_admin

# Préparer données pour camembert
labels_cat = list(totaux_cat.keys())
values_cat = list(totaux_cat.values())

fig_cat = px.pie(
    names=labels_cat,
    values=values_cat,
    title="Répartition globale des dépenses par catégorie",
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

st.plotly_chart(fig_cat, use_container_width=True)

# --- Graphique d'évolution du budget jour par jour (hors admin)


# Recalculer le budget par jour sans les coûts admin
def calc_budget_jour_sans_admin_ordered(data):
    budget_jour = []
    jour_global = 1

    for ville, jours in data.items():
        for _, details in jours.items():
            total = 0
            for cat in ["Activites", "Repas", "Transports"]:
                for elt in details.get(cat, []):
                    total += list(elt.values())[0]
            budget_jour.append((f"Jour {jour_global}", total))
            jour_global += 1

    return budget_jour


# Données pour graphique
budget_par_jour = calc_budget_jour_sans_admin_ordered(voyage_data)
jours = [item[0] for item in budget_par_jour]
montants = [item[1] for item in budget_par_jour]

# Tracer le graphique en courbe
fig_jours = px.line(
    x=jours,
    y=montants,
    markers=True,
    labels={"x": "Jour", "y": "Dépenses (€)"},
    title="Évolution des dépenses par jour (hors administratif)",
)

st.plotly_chart(fig_jours, use_container_width=True)
