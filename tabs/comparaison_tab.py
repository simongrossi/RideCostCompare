# tabs/comparaison_tab.py
import streamlit as st
import pandas as pd
import plotly.express as px
from dataclasses import asdict
from config import AppConfig
from charts import afficher_graphique_economies_cumulees
from utils import calculer_couts_voiture

def display_comparaison_tab(resultats_velo_min, resultats_velo_max, profil_data):
    """Affiche le contenu de l'onglet de comparaison avec une allocation des coûts par fourchette."""
    st.header("Analyse comparative du trajet domicile-travail")
    st.info("""
    La simulation est présentée sous forme de fourchette (min/max) basée sur votre usage du vélo.
    Le scénario **pessimiste** combine le coût le plus élevé du vélo avec le coût le plus bas de la voiture.
    Le scénario **optimiste** combine le coût le plus bas du vélo avec le coût le plus élevé de la voiture.
    """)

    if resultats_velo_min and resultats_velo_max and profil_data:
        # --- Fonction de calcul pour un scénario ---
        def calculer_cout_voiture_pour_trajet(km_velotaf, params_voiture):
            params_voiture.km_domicile_travail = km_velotaf
            resultats_voiture_scenario = calculer_couts_voiture(params_voiture)
            
            km_total = params_voiture.km_domicile_travail + params_voiture.km_autres
            proportion = km_velotaf / km_total if km_total > 0 else 0
            
            return resultats_voiture_scenario.cout_annuel * proportion

        # --- Calculs pour la fourchette ---
        params_voiture_base = st.session_state.voiture_params
        
        cout_voiture_min = calculer_cout_voiture_pour_trajet(resultats_velo_min.km_an, params_voiture_base)
        cout_voiture_max = calculer_cout_voiture_pour_trajet(resultats_velo_max.km_an, params_voiture_base)

        cout_velo_min = resultats_velo_min.cout_annuel_fmd
        cout_velo_max = resultats_velo_max.cout_annuel_fmd
        
        economie_min = cout_voiture_min - cout_velo_max  # Cas le plus défavorable
        economie_max = cout_voiture_max - cout_velo_min  # Cas le plus favorable
        
        # --- Affichage de la comparaison ---
        st.markdown("---")
        st.subheader("💰 Coût annuel du trajet (Fourchette Min-Max)")
        
        st.markdown("##### Coût du vélo")
        v_col1, v_col2 = st.columns(2)
        v_col1.metric("Min (optimiste)", f"{cout_velo_min:.0f}€")
        v_col2.metric("Max (pessimiste)", f"{cout_velo_max:.0f}€")

        st.markdown("##### Coût de la voiture (part allouée au trajet)")
        c_col1, c_col2 = st.columns(2)
        c_col1.metric("Min (usage faible)", f"{cout_voiture_min:.0f}€")
        c_col2.metric("Max (usage élevé)", f"{cout_voiture_max:.0f}€")

        st.markdown("---")
        st.subheader("✅ Économie annuelle finale")

        if economie_max > 0:
            eco_col1, eco_col2 = st.columns(2)
            eco_col1.metric("Économie minimale", f"{max(0, economie_min):.0f}€")
            eco_col2.metric("Économie maximale", f"{economie_max:.0f}€")
            
            st.markdown("---")
            st.subheader("✨ Vos gains en détail (basé sur un scénario moyen)")
            
            eco_moyenne = (economie_min + economie_max) / 2
            if eco_moyenne > 0:
                afficher_graphique_economies_cumulees(eco_moyenne)
            
            co2_economise_moyen = ((resultats_velo_min.km_an + resultats_velo_max.km_an) / 2 * AppConfig.CO2_VOITURE_G_PAR_KM) / 1000
            arbres_equivalents = co2_economise_moyen / AppConfig.CO2_ABSORPTION_ARBRE_KG_PAR_AN
            cafes_par_mois = (eco_moyenne / AppConfig.PRIX_MOYEN_CAFE) / 12

            g_col1, g_col2, g_col3 = st.columns(3)
            g_col1.metric("CO₂ économisé", f"~{co2_economise_moyen:.0f} kg/an")
            g_col2.metric("🌳 Équivalent Arbres", f"~{arbres_equivalents:.1f}")
            g_col3.metric("☕ Cafés offerts / mois", f"~{cafes_par_mois:.1f}")

        else:
            st.warning("Selon cette simulation, le vélo coûterait plus cher que la voiture, même dans le scénario le plus optimiste.")
    else:
        st.warning("Veuillez configurer un profil de vélo pour accéder à la comparaison.")