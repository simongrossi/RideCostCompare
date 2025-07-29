import streamlit as st
import json
import pandas as pd
from io import BytesIO
from dataclasses import asdict # <-- Ajout nécessaire pour la compatibilité avec les graphiques

# Import des fonctions locales et de la configuration
from utils import calculer_couts, calculer_couts_voiture
from charts import afficher_graphiques, afficher_camembert, afficher_camembert_comparatif
from config import AppConfig

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title=AppConfig.PAGE_TITLE, 
    layout=AppConfig.LAYOUT, 
    initial_sidebar_state=AppConfig.INITIAL_SIDEBAR_STATE
)

# --- Fonctions de gestion de données ---
def load_data(filepath=AppConfig.DEFAULT_PROFIL_VELO_FILE):
    """Charge les profils de vélo depuis un fichier JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Profil par défaut si le fichier n'existe pas ou est corrompu
        return {
            "Vélo Classique (700€)": {
                "prix_achat": 700, "aide": 50, "entretien_annuel": 80, 
                "duree": 6, "fmd": 300, "km_jour": 8.0, 
                "jours_semaine": 4, "aller_retour": True
            }
        }

def save_data(data, filepath=AppConfig.DEFAULT_PROFIL_VELO_FILE):
    """Sauvegarde les profils de vélo dans un fichier JSON."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde : {e}")
        return False

# --- Initialisation de l'état de la session ---
if 'profils_velo' not in st.session_state:
    st.session_state['profils_velo'] = load_data()
    st.session_state['profil_velo_actif'] = list(st.session_state.profils_velo.keys())[0]

if 'voiture_params' not in st.session_state:
    st.session_state['voiture_params'] = AppConfig.DEFAULT_VOITURE_PARAMS.copy()

# --- SIDEBAR (Contrôles du vélo) ---
with st.sidebar:
    st.title("RideCostCompare 🚲")
    st.header("Profil Vélo")
    profil_selectionne = st.selectbox(
        "Choisir un profil vélo", 
        list(st.session_state.profils_velo.keys()), 
        key='profil_selector'
    )

    if profil_selectionne != st.session_state.profil_velo_actif:
        st.session_state.profil_velo_actif = profil_selectionne
        st.rerun()

    profil_data = st.session_state.profils_velo[st.session_state.profil_velo_actif]
    
    with st.form(key='velo_form'):
        st.subheader("Paramètres du Vélo")
        p_achat = st.number_input("Prix d'achat (€)", value=profil_data.get("prix_achat", 0))
        p_aide = st.number_input("Aide à l'achat (€)", value=profil_data.get("aide", 0))
        p_entretien = st.number_input("Entretien annuel (€)", value=profil_data.get("entretien_annuel", 0))
        p_duree = st.number_input("Durée d'amortissement (ans)", value=profil_data.get("duree", 5))
        p_fmd = st.number_input("Forfait Mobilités Durables (€/an)", value=profil_data.get("fmd", 0))
        
        st.subheader("Paramètres de Déplacement")
        p_km_jour = st.number_input("Distance par trajet (km)", value=profil_data.get('km_jour', 0.0))
        p_aller_retour = st.checkbox("Trajet aller-retour ?", value=profil_data.get('aller_retour', True))
        p_jours_semaine = st.number_input("Jours par semaine", value=profil_data.get('jours_semaine', 3))
        
        submitted = st.form_submit_button('🔄 Appliquer les modifications')
        
        if submitted:
            profil_data.update({
                "prix_achat": p_achat, "aide": p_aide, "entretien_annuel": p_entretien, 
                "duree": p_duree, "fmd": p_fmd, "km_jour": p_km_jour, 
                "aller_retour": p_aller_retour, "jours_semaine": p_jours_semaine
            })
            if save_data(st.session_state.profils_velo):
                st.success("Profil sauvegardé !")

# --- Calculs Vélo ---
distance_trajet = profil_data['km_jour'] * (2 if profil_data['aller_retour'] else 1)
km_an_velo = distance_trajet * profil_data['jours_semaine'] * AppConfig.SEMAINES_TRAVAILLEES_PAR_AN
entretien_total_velo = profil_data['entretien_annuel'] * profil_data['duree']
resultats_velo = calculer_couts(
    profil_data['prix_achat'], profil_data['aide'], 
    entretien_total_velo, profil_data['duree'], 
    profil_data['fmd'], km_an_velo
)

# --- Définition des Onglets ---
tab_velo, tab_voiture, tab_comparaison = st.tabs(["🚲 Simulateur Vélo", "🚗 Simulateur Voiture", "📊 Tableau de Comparaison"])

# --- Onglet Vélo ---
with tab_velo:
    st.header(f"Analyse du coût pour : {st.session_state.profil_velo_actif}")
    col1, col2 = st.columns(2)
    with col1:
        # CORRECTION: Utilisation de l'accès par attribut
        st.metric("Coût annuel (après FMD)", f"{resultats_velo.cout_annuel_fmd:.2f} €")
        st.metric("Coût par km", f"{resultats_velo.cout_km_fmd:.2f} €")
    with col2:
        # CORRECTION: Utilisation de l'accès par attribut
        st.metric("Coût total sur la durée", f"{resultats_velo.cout_total_fmd:.2f} €")
        st.metric("Km parcourus par an", f"{km_an_velo:.0f} km")
    
    st.markdown("---")
    afficher_camembert(
        profil_data['prix_achat'], profil_data['aide'], 
        entretien_total_velo, profil_data['fmd'], profil_data['duree']
    )
    # CORRECTION: Conversion du dataclass en dictionnaire pour la fonction de graphique
    afficher_graphiques(asdict(resultats_velo))

# --- Onglet Voiture ---
with tab_voiture:
    st.header("Simulation du coût de la voiture")
    st.write("Renseignez ici les informations pour obtenir une estimation précise du coût annuel de votre voiture.")
    
    vp = st.session_state.voiture_params
    with st.form("car_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Coûts d'acquisition")
            vp['prix_achat'] = st.number_input("Prix d'achat (€)", value=vp['prix_achat'])
            vp['valeur_revente'] = st.number_input("Valeur de revente estimée (€)", value=vp['valeur_revente'])
            vp['duree_possession'] = st.number_input("Durée de possession (ans)", value=vp['duree_possession'], min_value=1)
            
            st.subheader("Coûts fixes annuels")
            vp['assurance'] = st.number_input("Assurance annuelle (€)", value=vp['assurance'])
            vp['entretien'] = st.number_input("Entretien annuel (€)", value=vp['entretien'])
            vp['autres_frais'] = st.number_input("Péages, parking, etc. (€/an)", value=vp['autres_frais'])
        
        with col2:
            st.subheader("Coûts variables")
            vp['km_annuels'] = st.number_input("Kilomètres annuels", value=vp.get('km_annuels', int(km_an_velo)))
            vp['consommation'] = st.number_input("Consommation (L/100km)", value=vp['consommation'])
            vp['prix_carburant'] = st.number_input("Prix du carburant (€/L)", value=vp['prix_carburant'], format="%.2f")

        car_submitted = st.form_submit_button("Calculer le coût de la voiture")

    # --- Calculs et affichage Voiture ---
    resultats_voiture = calculer_couts_voiture(vp)
    if car_submitted:
        st.success(f"Coût annuel de la voiture calculé !")

    st.header("Résultats pour la voiture")
    # CORRECTION: Utilisation de l'accès par attribut
    st.metric("Coût annuel total de la voiture", f"{resultats_voiture.cout_annuel:.2f} €")
    
    # CORRECTION: Utilisation de l'accès par attribut
    if resultats_voiture.details:
        df_car_details = pd.DataFrame.from_dict(resultats_voiture.details, orient='index', columns=['Coût Annuel (€)'])
        st.dataframe(df_car_details)

# --- Onglet Comparaison ---
with tab_comparaison:
    st.header("Synthèse de la comparaison")
    
    # CORRECTION: Utilisation de l'accès par attribut
    cout_velo = resultats_velo.cout_annuel_fmd
    cout_voiture = resultats_voiture.cout_annuel
    
    if cout_voiture > 0: # Éviter les divisions par zéro si la voiture n'est pas configurée
        economie_annuelle = cout_voiture - cout_velo
        co2_economise_kg = (vp['km_annuels'] * AppConfig.CO2_VOITURE_G_PAR_KM) / 1000

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Économie annuelle", f"{economie_annuelle:.0f} €", help="Différence entre le coût annuel de la voiture et celui du vélo (après FMD).")
        col2.metric("🌍 CO₂ économisé / an", f"{co2_economise_kg:.0f} kg", help=f"Basé sur {AppConfig.CO2_VOITURE_G_PAR_KM} gCO₂/km.")
        
        temps_rentabilite_mois = float('inf')
        if economie_annuelle > 0:
            cout_achat_net_velo = profil_data['prix_achat'] - profil_data['aide']
            if cout_achat_net_velo > 0:
                temps_rentabilite_mois = (cout_achat_net_velo / economie_annuelle) * 12
                col3.metric("📈 Point de rentabilité", f"{temps_rentabilite_mois:.1f} mois", help="Temps nécessaire pour que les économies remboursent le coût d'achat net du vélo.")

        st.markdown("---")
        
        # Préparation des données pour le graphique comparatif
        data_comparaison = {
            'cout_annuel_fmd': cout_velo,
            'km_an': vp['km_annuels'] # CORRECTION: Utilisation de l'attribut du résultat vélo
        }
        # Calcul du coût au km de la voiture pour la comparaison
        cout_voiture_km = cout_voiture / vp['km_annuels'] if vp['km_annuels'] > 0 else 0
        config_comparaison = {'COUT_VOITURE_KM': cout_voiture_km}
        
        afficher_camembert_comparatif(data_comparaison, "Voiture", config_comparaison)
    else:
        st.warning("Veuillez calculer le coût de la voiture dans l'onglet dédié pour afficher la comparaison.")