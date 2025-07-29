# tabs/comparaison_tab.py
import streamlit as st
from dataclasses import asdict
from config import AppConfig
from charts import afficher_camembert_comparatif, afficher_graphique_economies_cumulees
from export import export_pdf

def display_comparaison_tab(resultats_velo, profil_data):
    """Affiche le contenu de l'onglet de comparaison."""
    st.header("Synthèse de la comparaison")
    if resultats_velo and profil_data:
        resultats_voiture = st.session_state.resultats_voiture
        cout_velo = resultats_velo.cout_annuel_fmd
        cout_voiture = resultats_voiture.cout_annuel
        
        if cout_voiture > 0 and cout_velo < cout_voiture:
            economie_annuelle = cout_voiture - cout_velo
            
            st.subheader("🎉 Vos gains annuels en passant au vélo")
            col1, col2 = st.columns(2)
            col1.metric("Économie financière", f"{economie_annuelle:.2f} €/an")
            
            co2_economise_kg = (resultats_velo.km_an * AppConfig.CO2_VOITURE_G_PAR_KM) / 1000
            col2.metric("CO₂ économisé", f"{co2_economise_kg:.2f} kg/an")
            
            st.subheader("✨ C'est l'équivalent de...")
            c1, c2, c3 = st.columns(3)
            arbres_equivalents = co2_economise_kg / AppConfig.CO2_ABSORPTION_ARBRE_KG_PAR_AN
            c1.metric("🌳 Arbres plantés", f"{arbres_equivalents:.1f}")
            
            cafes_par_mois = (economie_annuelle / AppConfig.PRIX_MOYEN_CAFE) / 12
            c2.metric("☕ Cafés offerts par mois", f"{cafes_par_mois:.1f}")
            
            # Calcul de rentabilité corrigé
            investissement_initial = profil_data.get('prix_achat', 0) - profil_data.get('aide', 0)
            duree_rentabilite_mois = (investissement_initial / economie_annuelle) * 12 if economie_annuelle > 0 else 'N/A'
            if isinstance(duree_rentabilite_mois, float):
                c3.metric("Vélo rentabilisé en", f"{duree_rentabilite_mois:.1f} mois")

            st.markdown("---")
            
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
                with st.spinner("Création du PDF en cours..."):
                    export_data = asdict(resultats_velo)
                    export_data.update({
                        'cout_annuel_voiture': cout_voiture,
                        'economie_annuelle_vs_voiture': economie_annuelle,
                        'co2_economise_par_an': co2_economise_kg
                    })
                    
                    img_bytes = fig_camembert.to_image(format="png", engine="kaleido") if fig_camembert and fig_camembert.data else None
                    pdf_filename = export_pdf(export_data, img_bytes)
                    
                    with open(pdf_filename, "rb") as pdf_file:
                        st.download_button(
                            label="✔️ Télécharger le PDF",
                            data=pdf_file,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )
        elif cout_voiture <= cout_velo:
             st.info("Le coût annuel du vélo est actuellement supérieur ou égal à celui de la voiture. Modifiez les paramètres pour réaliser des économies.")
        else:
            st.info("Calculez d'abord le coût de la voiture dans l'onglet dédié pour voir la comparaison.")
    else:
        st.warning("Veuillez configurer un profil de vélo pour accéder à la comparaison.")