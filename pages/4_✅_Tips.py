import streamlit as st

# Exemple de données
data = [
    {"id": 1, "name": "Ligne A", "value": 10},
    {"id": 2, "name": "Ligne B", "value": 20},
    {"id": 3, "name": "Ligne C", "value": 30},
]

st.title("Menu trois points avec édition")

# Pour stocker les données modifiées
if "data" not in st.session_state:
    st.session_state.data = data.copy()

for item in st.session_state.data:
    col1, col2 = st.columns([6, 1])  # Ligne + menu trois points
    with col1:
        st.write(f"**{item['name']}** — {item['value']}")
    with col2:
        with st.popover("⋮"):
            st.write("Options")
            # Bouton éditer
            if st.button(f"✏️ Éditer {item['id']}", key=f"edit-{item['id']}"):
                # Afficher le formulaire d'édition
                with st.popover(f"Éditer {item['name']}", use_container_width=True):
                    with st.form(f"form-{item['id']}"):
                        new_name = st.text_input("Nom", item['name'])
                        new_value = st.number_input("Valeur", value=item['value'])
                        submitted = st.form_submit_button("✅ Sauvegarder")
                        if submitted:
                            # Mettre à jour la ligne
                            item['name'] = new_name
                            item['value'] = new_value
                            st.success(f"Ligne {item['id']} mise à jour ✅")
                            st.experimental_rerun()

            # Bouton supprimer
            if st.button(f"🗑️ Supprimer {item['id']}", key=f"delete-{item['id']}"):
                st.session_state.data = [
                    i for i in st.session_state.data if i['id'] != item['id']
                ]
                st.warning(f"Ligne {item['id']} supprimée ❌")
                st.rerun()
