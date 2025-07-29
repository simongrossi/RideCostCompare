# tabs/voiture_tab.py
import streamlit as st
import pandas as pd
from utils import calculer_couts_voiture, VoitureParams
from charts import afficher_camembert_repartition

def display_voiture_tab():
    """Affiche le contenu de l'onglet du simulateur voiture."""
    st.header("Simulation du coût de la voiture")
    
    vp = st.session_state.voiture_params 
    with st.form("car_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Coûts d'acquisition")
            vp.prix_achat = st.number_input("Prix d'achat (€)", value=vp.prix_achat, min_value=0)
            vp.valeur_revente = st.number_input("Valeur de revente (€)", value=vp.valeur_revente, min_value=0)
            vp.duree_possession = st.number_input("Durée de possession (ans)", value=vp.duree_possession, min_value=1)
            
            st.subheader("Coûts fixes annuels")
            vp.assurance = st.number_input("Assurance annuelle (€)", value=vp.assurance, min_value=0)
            vp.entretien = st.number_input("Entretien annuel (€)", value=vp.entretien, min_value=0)
            vp.autres_frais = st.number_input("Autres frais annuels (€)", value=vp.autres_frais, min_value=0)

        with col2:
            st.subheader("Coûts variables")
            vp.km_annuels = st.number_input("Kilométrage annuel (km)", value=vp.km_annuels, min_value=0)
            vp.consommation = st.number_input("Consommation (L/100km)", value=vp.consommation, min_value=0.0, format="%.2f")
            vp.prix_carburant = st.number_input("Prix du carburant (€/L)", value=vp.prix_carburant, min_value=0.0, format="%.2f")
        
        b_col1, b_col2, _ = st.columns([1, 1, 3])
        with b_col1:
            car_submitted = st.form_submit_button("🔄 Calculer le coût")
        with b_col2:
            car_reset = st.form_submit_button("Réinitialiser")

    if car_submitted:
        st.session_state.resultats_voiture = calculer_couts_voiture(vp)
        st.success("Coût de la voiture recalculé !")
        st.rerun()

    if car_reset:
        st.session_state.voiture_params = VoitureParams()
        st.session_state.resultats_voiture = calculer_couts_voiture(st.session_state.voiture_params)
        st.info("Les paramètres de la voiture ont été réinitialisés.")
        st.rerun()

    resultats_voiture = st.session_state.resultats_voiture
    st.header("Résultats pour la voiture")
    
    col1, col2 = st.columns(2)
    col1.metric("Coût annuel total", f"{resultats_voiture.cout_annuel:.2f} €")
    col2.metric("Coût par km", f"{resultats_voiture.cout_km:.3f} €")
    
    amortissement = resultats_voiture.details.get("Amortissement", 0)
    couts_fixes_hors_amort = resultats_voiture.details.get("Assurance", 0) + resultats_voiture.details.get("Entretien", 0) + resultats_voiture.details.get("Autres frais", 0)
    cout_inactivite = amortissement + couts_fixes_hors_amort
    
    st.metric("Coût de l'inactivité (annuel)", f"{cout_inactivite:.2f} €", 
              help="Coût des frais fixes (amortissement, assurance, etc.) même si la voiture ne roule pas.")

    st.markdown("---")
    
    st.subheader("Répartition des coûts annuels de la voiture")
    afficher_camembert_repartition(resultats_voiture.details, "Répartition du coût annuel de la voiture")