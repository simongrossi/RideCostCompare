# tabs/comparaison_tab.py
import streamlit as st
from dataclasses import asdict
from config import AppConfig
from charts import afficher_camembert_comparatif
from export import export_pdf

def display_comparaison_tab(resultats_velo):
    """Affiche le contenu de l'onglet de comparaison."""
    st.header("Synthèse de la comparaison")
    if resultats_velo:
        resultats_voiture = st.session_state.resultats_voiture
        cout_velo = resultats_velo.cout_annuel_fmd
        cout_voiture = resultats_voiture.cout_annuel
        
        if cout_voiture > 0:
            economie_annuelle = cout_voiture - cout_velo
            vp = st.session_state.voiture_params
            co2_economise_kg = (vp.km_annuels * AppConfig.CO2_VOITURE_G_PAR_KM) / 1000

            col1, col2, col3 = st.columns(3)
            col1.metric("Économie vs Voiture", f"{economie_annuelle:.2f} €/an")
            col2.metric("Point de rentabilité", f"{12 * resultats_velo.cout_total / economie_annuelle if economie_annuelle > 0 else 'N/A'} mois")
            col3.metric("CO₂ économisé", f"{co2_economise_kg:.2f} kg/an")

            st.markdown("---")
            
            data_comparaison = {'cout_annuel_fmd': cout_velo, 'km_an': vp.km_annuels}
            cout_voiture_km = cout_voiture / vp.km_annuels if vp.km_annuels > 0 else 0
            config_comparaison = {'COUT_VOITURE_KM': cout_voiture_km}
            
            # Affichage du graphique
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
                    
                    img_bytes = fig_camembert.to_image(format="png", engine="kaleido") if fig_camembert.data else None
                    pdf_filename = export_pdf(export_data, img_bytes)
                    
                    with open(pdf_filename, "rb") as pdf_file:
                        st.download_button(
                            label="✔️ Télécharger le PDF",
                            data=pdf_file,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )
        else:
            st.info("Calculez d'abord le coût de la voiture dans l'onglet dédié pour voir la comparaison.")
    else:
        st.warning("Veuillez configurer un profil de vélo pour accéder à la comparaison.")