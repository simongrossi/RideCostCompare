# tabs/comparaison_tab.py
import streamlit as st
from dataclasses import asdict
from config import AppConfig
from charts import afficher_camembert_comparatif, afficher_graphique_economies_cumulees
from export import export_pdf

def display_comparaison_tab(resultats_velo):
    """Affiche le contenu de l'onglet de comparaison."""
    st.header("Synthèse de la comparaison")
    if resultats_velo:
        resultats_voiture = st.session_state.resultats_voiture
        cout_velo = resultats_velo.cout_annuel_fmd
        cout_voiture = resultats_voiture.cout_annuel
        
        if cout_voiture > 0 and cout_velo < cout_voiture:
            economie_annuelle = cout_voiture - cout_velo
            
            st.subheader("🎉 Vos gains annuels en passant au vélo")
            col1, col2 = st.columns(2)
            col1.metric("Économie financière", f"{economie_annuelle:.2f} €/an")
            
            # Calculs pour les nouvelles stats
            co2_economise_kg = (resultats_velo.km_an * AppConfig.CO2_VOITURE_G_PAR_KM) / 1000
            arbres_equivalents = co2_economise_kg / AppConfig.CO2_ABSORPTION_ARBRE_KG_PAR_AN
            cafes_par_mois = (economie_annuelle / AppConfig.PRIX_MOYEN_CAFE) / 12

            col2.metric("CO₂ économisé", f"{co2_economise_kg:.2f} kg/an")
            
            st.subheader("✨ C'est l'équivalent de...")
            c1, c2, c3 = st.columns(3)
            c1.metric("🌳 Arbres plantés", f"{arbres_equivalents:.1f}")
            c2.metric("☕ Cafés offerts par mois", f"{cafes_par_mois:.1f}")
            
            # Point de rentabilité du vélo
            duree_rentabilite_mois = (resultats_velo.cout_total - resultats_velo.duree * resultats_velo.cout_annuel_fmd) / economie_annuelle * 12 if economie_annuelle > 0 else 'N/A'
            if isinstance(duree_rentabilite_mois, float):
                c3.metric("Vélo rentabilisé en", f"{duree_rentabilite_mois:.1f} mois")

            st.markdown("---")
            
            # Graphiques
            st.subheader("Visualisations")
            afficher_graphique_economies_cumulees(economie_annuelle)
            
            data_comparaison = {'cout_annuel_fmd': cout_velo, 'km_an': resultats_velo.km_an}
            config_comparaison = {'COUT_VOITURE_KM': resultats_voiture.cout_km}
            fig_camembert = afficher_camembert_comparatif(data_comparaison, "Voiture", config_comparaison, return_fig=True)
            if fig_camembert:
                st.plotly_chart(fig_camembert, use_container_width=True)

            st.markdown("---")
            st.subheader("📥 Exporter le rapport")
            
            if st.button("Générer le rapport PDF"):
                # ... (logique d'export inchangée) ...

        elif cout_voiture <= cout_velo:
             st.info("Le coût annuel du vélo est actuellement supérieur ou égal à celui de la voiture. Modifiez les paramètres pour réaliser des économies.")
        else:
            st.info("Calculez d'abord le coût de la voiture dans l'onglet dédié pour voir la comparaison.")
    else:
        st.warning("Veuillez configurer un profil de vélo pour accéder à la comparaison.")