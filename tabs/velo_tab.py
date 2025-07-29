# tabs/velo_tab.py
import streamlit as st
from charts import afficher_graphiques, afficher_camembert, afficher_tableau_details

def display_velo_tab(resultats_velo, profil_actif):
    """Affiche le contenu de l'onglet du simulateur vélo."""
    if resultats_velo:
        st.header(f"Analyse du coût pour : {profil_actif}")

        # Conversion du dataclass en dictionnaire pour l'affichage
        resultats_dict = resultats_velo.__dict__

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Coût Annuel (avec FMD)", f"{resultats_dict['cout_annuel_fmd']:.2f} €")
            st.metric("Coût par km (avec FMD)", f"{resultats_dict['cout_km_fmd']:.2f} €")
        with col2:
            st.metric("Kilométrage annuel", f"{resultats_dict['km_an']} km")
            st.metric("Coût Total sur la durée", f"{resultats_dict['cout_total_fmd']:.2f} €")
        
        st.markdown("---")
        
        afficher_graphiques(resultats_dict)
        afficher_tableau_details(resultats_dict)
        
    else:
        st.info("👋 Bienvenue ! Veuillez commencer par créer un profil de vélo dans le menu latéral.")