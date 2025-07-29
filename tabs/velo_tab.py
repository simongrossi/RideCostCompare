# tabs/velo_tab.py
import streamlit as st
from config import AppConfig
from charts import afficher_graphiques, afficher_tableau_details, afficher_camembert_repartition

def display_velo_tab(resultats_velo, profil_actif):
    """Affiche le contenu de l'onglet du simulateur vélo."""
    if resultats_velo and profil_actif:
        profil_data = st.session_state.profils_velo[profil_actif]
        st.header(f"Analyse du coût pour : {profil_actif}")
        resultats_dict = resultats_velo.__dict__

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Coût Annuel (avec FMD)", f"{resultats_dict['cout_annuel_fmd']:.2f} €")
            st.metric("Coût par km (avec FMD)", f"{resultats_dict['cout_km_fmd']:.2f} €")
        with col2:
            st.metric("Kilométrage annuel", f"{resultats_dict['km_an']} km")
            st.metric("Coût Total sur la durée", f"{resultats_dict['cout_total_fmd']:.2f} €")
        
        st.subheader("Coûts par période")
        jours_travailles = profil_data.get('jours_semaine', 0) * AppConfig.SEMAINES_TRAVAILLEES_PAR_AN
        cout_mensuel = resultats_velo.cout_annuel_fmd / 12
        cout_jour_travaille = resultats_velo.cout_annuel_fmd / jours_travailles if jours_travailles > 0 else 0
        col_a, col_b = st.columns(2)
        col_a.metric("Coût mensuel moyen", f"{cout_mensuel:.2f} €")
        col_b.metric("Coût par jour travaillé", f"{cout_jour_travaille:.2f} €")

        st.markdown("---")
        afficher_graphiques(resultats_dict)
        
        st.subheader("Répartition des coûts du vélo")
        duree = profil_data.get('duree', 1)
        entretien = profil_data.get('entretien_annuel', 0) * duree
        achat_net = resultats_velo.cout_total - entretien
        details_velo = {"Achat net (achat - aide)": achat_net, "Entretien total sur la durée": entretien}
        afficher_camembert_repartition(details_velo, "Répartition du coût total du vélo (hors FMD)")

        st.markdown("---")
        afficher_tableau_details(resultats_dict)
        
    else:
        st.info("👋 Bienvenue ! Veuillez commencer par créer un profil de vélo dans le menu latéral.")