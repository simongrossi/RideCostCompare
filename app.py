import streamlit as st
import json
import pandas as pd
from dataclasses import asdict

# Import des fonctions locales et de la configuration
from utils import calculer_couts, calculer_couts_voiture, VoitureParams
from charts import afficher_graphiques, afficher_camembert, afficher_camembert_comparatif
from config import AppConfig
from export import export_pdf

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

        profil_data = st.session_state.profils_velo[st.session_state.profil_velo_actif]
        
        with st.form(key='velo_form'):
            # ... (contenu du formulaire vélo inchangé) ...
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
                # ... (logique de sauvegarde inchangée) ...
                st.success("Profil sauvegardé !")

# --- Calculs Vélo ---
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
else:
    resultats_velo = None

# --- Définition des Onglets ---
tab_velo, tab_voiture, tab_comparaison = st.tabs(["🚲 Simulateur Vélo", "🚗 Simulateur Voiture", "📊 Tableau de Comparaison"])

# --- Onglet Vélo ---
with tab_velo:
    if resultats_velo:
        st.header(f"Analyse du coût pour : {st.session_state.profil_velo_actif}")
        # ... (contenu de l'onglet vélo inchangé)
    else:
        st.info("👋 Bienvenue ! Veuillez commencer par créer un profil de vélo dans le menu latéral.")

# --- Onglet Voiture ---
with tab_voiture:
    st.header("Simulation du coût de la voiture")
    vp = st.session_state.voiture_params 
    with st.form("car_form"):
        # ... (contenu du formulaire voiture inchangé) ...
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Coûts d'acquisition")
            vp.prix_achat = st.number_input("Prix d'achat (€)", value=vp.prix_achat)
            # ... (autres inputs) ...
        with col2:
            st.subheader("Coûts variables")
            # ... (autres inputs) ...
        
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
    st.metric("Coût annuel total de la voiture", f"{resultats_voiture.cout_annuel:.2f} €")
    if resultats_voiture.details:
        df_car_details = pd.DataFrame.from_dict(resultats_voiture.details, orient='index', columns=['Coût Annuel (€)'])
        st.dataframe(df_car_details)

# --- Onglet Comparaison ---
with tab_comparaison:
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
            # ... (métriques inchangées) ...

            st.markdown("---")
            
            data_comparaison = {'cout_annuel_fmd': cout_velo, 'km_an': vp.km_annuels}
            cout_voiture_km = cout_voiture / vp.km_annuels if vp.km_annuels > 0 else 0
            config_comparaison = {'COUT_VOITURE_KM': cout_voiture_km}
            
            afficher_camembert_comparatif(data_comparaison, "Voiture", config_comparaison)

            st.markdown("---")
            st.subheader("📥 Exporter le rapport")
            
            if st.button("Générer le rapport PDF"):
                with st.spinner("Création du PDF en cours..."):
                    # Préparer les données pour le PDF
                    export_data = asdict(resultats_velo)
                    export_data.update({
                        'cout_annuel_voiture': cout_voiture,
                        'economie_annuelle_vs_voiture': economie_annuelle,
                        'co2_economise_par_an': co2_economise_kg
                    })
                    
                    fig = afficher_camembert_comparatif(data_comparaison, "Voiture", config_comparaison, return_fig=True)
                    img_bytes = fig.to_image(format="png", engine="kaleido") if fig.data else None
                    
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