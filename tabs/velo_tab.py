# tabs/velo_tab.py
import streamlit as st
from config import AppConfig
from charts import afficher_tableau_details, afficher_camembert_repartition

def display_velo_tab(resultats_velo_min, resultats_velo_max, profil_actif):
    """Affiche le contenu de l'onglet du simulateur vélo."""
    if resultats_velo_min and resultats_velo_max and profil_actif:
        profil_data = st.session_state.profils_velo[profil_actif]
        st.header(f"Analyse du coût pour : {profil_actif}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Coût Annuel (avec FMD)", 
                f"{resultats_velo_min.cout_annuel_fmd:.0f}€ - {resultats_velo_max.cout_annuel_fmd:.0f}€"
            )
            st.metric(
                "Coût par km (avec FMD)",
                f"{resultats_velo_min.cout_km_fmd:.2f}€ - {resultats_velo_max.cout_km_fmd:.2f}€"
            )
        with col2:
            st.metric(
                "Kilométrage annuel", 
                f"{resultats_velo_min.km_an} km - {resultats_velo_max.km_an} km"
            )
            st.metric(
                "Coût Total sur la durée",
                f"{resultats_velo_min.cout_total_fmd:.0f}€ - {resultats_velo_max.cout_total_fmd:.0f}€"
            )
        
        st.markdown("---")
        st.subheader("Répartition des coûts du vélo")
        duree = profil_data.get('duree', 1)
        entretien = profil_data.get('entretien_annuel', 0) * duree
        achat_net = resultats_velo_min.cout_total - entretien
        details_velo = {"Achat net (achat - aide)": achat_net, "Entretien total sur la durée": entretien}
        afficher_camembert_repartition(details_velo, "Répartition du coût total du vélo (hors FMD)")

    else:
        st.info("👋 Bienvenue ! Veuillez commencer par créer un profil de vélo dans le menu latéral.")