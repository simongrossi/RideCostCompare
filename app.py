# app.py
import streamlit as st
import json
from dataclasses import asdict

# Import des fonctions locales et de la configuration
from utils import calculer_couts, calculer_couts_voiture, VoitureParams
from config import AppConfig

# Import des modules pour chaque onglet
from tabs.velo_tab import display_velo_tab
from tabs.voiture_tab import display_voiture_tab
from tabs.comparaison_tab import display_comparaison_tab

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
        return {}

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
    st.session_state['profil_velo_actif'] = list(st.session_state.profils_velo.keys())[0] if st.session_state.profils_velo else None

if 'voiture_params' not in st.session_state:
    st.session_state['voiture_params'] = VoitureParams()

if 'resultats_voiture' not in st.session_state:
    st.session_state['resultats_voiture'] = calculer_couts_voiture(st.session_state.voiture_params)

# --- SIDEBAR (Contrôles du vélo) ---
with st.sidebar:
    st.title("RideCostCompare 🚲")
    st.header("Profil Vélo")
    if st.session_state.profils_velo:
        profil_selectionne = st.selectbox(
            "Choisir un profil vélo", 
            list(st.session_state.profils_velo.keys()), 
            key='profil_selector'
        )

        if profil_selectionne != st.session_state.profil_velo_actif:
            st.session_state.profil_velo_actif = profil_selectionne
            st.rerun()

        profil_data_sidebar = st.session_state.profils_velo.get(st.session_state.profil_velo_actif, {})
        
        with st.form(key='velo_form'):
            st.subheader("Paramètres du Vélo")
            p_achat = st.number_input("Prix d'achat (€)", value=profil_data_sidebar.get("prix_achat", 0))
            p_aide = st.number_input("Aide à l'achat (€)", value=profil_data_sidebar.get("aide", 0))
            p_entretien = st.number_input("Entretien annuel (€)", value=profil_data_sidebar.get("entretien_annuel", 0))
            p_duree = st.number_input("Durée d'amortissement (ans)", value=profil_data_sidebar.get("duree", 5), min_value=1)
            p_fmd = st.number_input("Forfait Mobilités Durables (€/an)", value=profil_data_sidebar.get("fmd", 0))
            
            st.subheader("Paramètres de Déplacement")
            p_km_jour = st.number_input("Distance par trajet (km)", value=profil_data_sidebar.get('km_jour', 0.0))
            p_aller_retour = st.checkbox("Trajet aller-retour ?", value=profil_data_sidebar.get('aller_retour', True))
            p_jours_semaine = st.number_input("Jours par semaine", value=profil_data_sidebar.get('jours_semaine', 3))
            
            submitted = st.form_submit_button('🔄 Appliquer les modifications')
            if submitted:
                updated_data = {
                    "prix_achat": p_achat, "aide": p_aide, "entretien_annuel": p_entretien,
                    "duree": p_duree, "fmd": p_fmd, "km_jour": p_km_jour,
                    "aller_retour": p_aller_retour, "jours_semaine": p_jours_semaine
                }
                st.session_state.profils_velo[st.session_state.profil_velo_actif] = updated_data
                if save_data(st.session_state.profils_velo):
                    st.success("Profil sauvegardé !")
                st.rerun()

# --- Calculs principaux ---
resultats_velo = None
profil_data = None  # Initialisation à None
if st.session_state.profil_velo_actif:
    profil_data = st.session_state.profils_velo[st.session_state.profil_velo_actif]
    distance_trajet = profil_data['km_jour'] * (2 if profil_data['aller_retour'] else 1)
    km_an_velo = distance_trajet * profil_data['jours_semaine'] * AppConfig.SEMAINES_TRAVAILLEES_PAR_AN
    entretien_total_velo = profil_data['entretien_annuel'] * profil_data['duree']
    resultats_velo = calculer_couts(
        profil_data['prix_achat'], profil_data['aide'], 
        entretien_total_velo, profil_data['duree'], 
        profil_data['fmd'], km_an_velo
    )

# --- Définition et affichage des onglets ---
tab_velo, tab_voiture, tab_comparaison = st.tabs(["🚲 Simulateur Vélo", "🚗 Simulateur Voiture", "📊 Tableau de Comparaison"])

with tab_velo:
    display_velo_tab(resultats_velo, st.session_state.get('profil_velo_actif', ''))

with tab_voiture:
    display_voiture_tab()

with tab_comparaison:
    # On passe maintenant profil_data en plus de resultats_velo
    display_comparaison_tab(resultats_velo, profil_data)