# tabs/voiture_tab.py
import streamlit as st
import pandas as pd
from utils import calculer_couts_voiture, VoitureParams
from charts import afficher_camembert_repartition
from config import AppConfig

def display_voiture_tab():
    """Affiche le contenu de l'onglet du simulateur voiture."""
    st.header("Simulation du coût global de la voiture")
    st.info("Saisissez ici les coûts fixes de votre voiture et estimez vos trajets personnels.")

    vp = st.session_state.voiture_params 
    with st.form("car_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Coûts d'acquisition et fixes")
            vp.prix_achat = st.number_input("Prix d'achat (€)", value=vp.prix_achat, min_value=0)
            vp.valeur_revente = st.number_input("Valeur de revente (€)", value=vp.valeur_revente, min_value=0)
            vp.duree_possession = st.number_input("Durée de possession (ans)", value=vp.duree_possession, min_value=1)
            vp.assurance = st.number_input("Assurance annuelle (€)", value=vp.assurance, min_value=0)
            vp.entretien = st.number_input("Entretien annuel (€)", value=vp.entretien, min_value=0)
            vp.autres_frais = st.number_input("Autres frais annuels (€)", value=vp.autres_frais, min_value=0)

        with col2:
            st.subheader("Estimation des trajets personnels")
            nb_trajets_courts = st.number_input("Nb. trajets courts / semaine (ex: courses)", value=4, min_value=0)
            dist_trajet_court = st.number_input("Distance A/R d'un trajet court (km)", value=10, min_value=0)
            nb_trajets_longs = st.number_input("Nb. trajets longs / semaine (ex: loisirs)", value=1, min_value=0)
            dist_trajet_long = st.number_input("Distance A/R d'un trajet long (km)", value=50, min_value=0)
            
            st.subheader("Consommation")
            vp.consommation = st.number_input("Consommation (L/100km)", value=vp.consommation, min_value=0.0, format="%.2f")
            vp.prix_carburant = st.number_input("Prix du carburant (€/L)", value=vp.prix_carburant, min_value=0.0, format="%.2f")
        
        b_col1, b_col2, _ = st.columns([1, 1, 3])
        with b_col1:
            car_submitted = st.form_submit_button("🔄 Recalculer")
        with b_col2:
            car_reset = st.form_submit_button("Réinitialiser")

    semaines_perso = 52
    km_autres_calcules = (nb_trajets_courts * dist_trajet_court + nb_trajets_longs * dist_trajet_long) * semaines_perso
    
    if car_submitted:
        vp.km_autres = km_autres_calcules
        st.session_state.voiture_params = vp
        st.success("Paramètres de la voiture mis à jour !")
        st.rerun()

    if car_reset:
        st.session_state.voiture_params = VoitureParams()
        st.info("Les paramètres de la voiture ont été réinitialisés.")
        st.rerun()
    
    voiture_params_actuels = st.session_state.voiture_params
    voiture_params_actuels.km_autres = km_autres_calcules
    resultats_voiture_globaux = calculer_couts_voiture(voiture_params_actuels)
    
    st.header("Résultats globaux pour la voiture")
    st.info(f"Le kilométrage des trajets personnels ('autres') est estimé à **{km_autres_calcules} km/an**.")
    
    r_col1, r_col2 = st.columns(2)
    r_col1.metric("Coût annuel total (hors vélotaf)", f"{resultats_voiture_globaux.cout_annuel:.2f} €")
    r_col2.metric("Coût par km (moyen)", f"{resultats_voiture_globaux.cout_km:.3f} €")
    
    st.markdown("---")
    
    st.subheader("Répartition des coûts annuels (trajets personnels uniquement)")
    afficher_camembert_repartition(resultats_voiture_globaux.details, "Répartition du coût annuel de la voiture")