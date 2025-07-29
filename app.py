import streamlit as st
import json
import pandas as pd
from io import BytesIO

# Import des fonctions locales
from charts import afficher_graphiques, afficher_comparaison, afficher_camembert, afficher_camembert_comparatif, afficher_tableau_details
from utils import calculer_couts

# --- Configuration et Constantes par défaut ---
# Ces valeurs seront modifiables par l'utilisateur dans l'interface
DEFAULT_CONFIG = {
    "COUT_NAVIGO_ANNUEL": 1036.80,
    "COUT_VOITURE_KM": 0.45,
    "SEMAINES_TRAVAILLEES": 45,
    "CO2_VOITURE_G_PAR_KM": 120
}

st.set_page_config(page_title="RideCostCompare", layout="wide", initial_sidebar_state="expanded")

# --- Fonctions de gestion de profils (lecture/écriture) ---
def load_data(filepath='profils.json'):
    """Charge les profils depuis un fichier JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Vélo par défaut": {"prix_achat": 1000, "aide": 300, "entretien_annuel": 150, "duree": 5, "fmd": 200, "km_jour": 8.0, "jours_semaine": 5, "aller_retour": True}}

def save_data(data, filepath='profils.json'):
    """Sauvegarde les profils dans un fichier JSON."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde : {e}")
        return False

# --- Initialisation de l'état de la session ---
if 'profils' not in st.session_state:
    st.session_state['profils'] = load_data()
    st.session_state['profil_actif'] = list(st.session_state['profils'].keys())[0]
if 'config' not in st.session_state:
    st.session_state['config'] = DEFAULT_CONFIG.copy()

# --- INTERFACE UTILISATEUR (SIDEBAR) ---
st.sidebar.title("RideCostCompare 🚲")
st.sidebar.markdown("Un simulateur pour calculer le coût réel de vos déplacements à vélo.")

# --- Section de gestion des profils ---
st.sidebar.markdown("### 👤 Profils d'utilisateur")
profil_selectionne = st.sidebar.selectbox(
    "Choisir un profil",
    list(st.session_state['profils'].keys()),
    index=list(st.session_state['profils'].keys()).index(st.session_state.get('profil_actif', 0)),
    key='profil_selector'
)
if profil_selectionne != st.session_state['profil_actif']:
    st.session_state['profil_actif'] = profil_selectionne
    st.rerun()

profil_data = st.session_state['profils'][st.session_state['profil_actif']]

# --- Formulaire pour les paramètres du vélo ---
with st.sidebar.form(key='params_form'):
    st.markdown("#### 🛠️ Paramètres du vélo")
    p_achat = st.number_input("Prix d'achat (€)", min_value=0, value=profil_data.get("prix_achat", 0))
    p_aide = st.number_input("Aide à l'achat (€)", min_value=0, value=profil_data.get("aide", 0))
    p_entretien = st.number_input("Entretien annuel (€)", min_value=0, value=profil_data.get("entretien_annuel", 0))
    p_duree = st.number_input("Durée d'amortissement (ans)", min_value=1, value=profil_data.get("duree", 5))
    p_fmd = st.number_input("Forfait Mobilités Durables (€/an)", min_value=0, value=profil_data.get("fmd", 0))

    st.markdown("#### 📏 Paramètres de déplacement")
    p_km_jour = st.number_input("Distance par trajet (km)", min_value=0.0, value=profil_data.get('km_jour', 0.0), format="%.2f")
    p_aller_retour = st.checkbox("Le trajet est un aller-retour ?", value=profil_data.get('aller_retour', True))
    p_jours_semaine = st.number_input("Jours travaillés par semaine", min_value=0, max_value=7, value=profil_data.get('jours_semaine', 3))
    
    submitted = st.form_submit_button('🔄 Mettre à jour les calculs')

# --- Mise à jour des données du profil actif (sans sauvegarder) ---
if submitted:
    profil_data.update({
        "prix_achat": p_achat, "aide": p_aide, "entretien_annuel": p_entretien, "duree": p_duree,
        "fmd": p_fmd, "km_jour": p_km_jour, "aller_retour": p_aller_retour, "jours_semaine": p_jours_semaine
    })

# --- Actions sur les profils (sauvegarder, créer, supprimer) ---
st.sidebar.markdown("---")
st.sidebar.markdown("#### 💾 Gérer les profils")

if st.sidebar.button("Enregistrer les modifications"):
    if save_data(st.session_state['profils']):
        st.sidebar.success(f"Profil '{st.session_state['profil_actif']}' sauvegardé !")

with st.sidebar.expander("➕ Créer un nouveau profil"):
    new_profile_name = st.text_input("Nom du nouveau profil")
    if st.button("Créer et sauvegarder"):
        if new_profile_name:
            if new_profile_name not in st.session_state['profils']:
                st.session_state['profils'][new_profile_name] = profil_data.copy()
                if save_data(st.session_state['profils']):
                    st.session_state['profil_actif'] = new_profile_name
                    st.success(f"Profil '{new_profile_name}' créé !")
                    st.rerun()
            else:
                st.warning("Ce nom de profil existe déjà.")
        else:
            st.warning("Veuillez donner un nom au profil.")

if st.sidebar.button("🗑️ Supprimer le profil actif", type="secondary"):
    if len(st.session_state['profils']) > 1:
        del st.session_state['profils'][st.session_state['profil_actif']]
        if save_data(st.session_state['profils']):
            st.session_state['profil_actif'] = list(st.session_state['profils'].keys())[0]
            st.warning(f"Profil supprimé. Passage au profil '{st.session_state['profil_actif']}'.")
            st.rerun()
    else:
        st.error("Impossible de supprimer le dernier profil.")

# --- Paramètres de comparaison avancés ---
with st.sidebar.expander("⚙️ Paramètres de comparaison"):
    st.session_state.config['COUT_VOITURE_KM'] = st.number_input("Coût au km de la voiture (€)", value=st.session_state.config.get('COUT_VOITURE_KM', 0.45))
    st.session_state.config['COUT_NAVIGO_ANNUEL'] = st.number_input("Coût annuel des transports (€)", value=st.session_state.config.get('COUT_NAVIGO_ANNUEL', 1036.80))
    st.session_state.config['SEMAINES_TRAVAILLEES'] = st.number_input("Semaines travaillées par an", value=st.session_state.config.get('SEMAINES_TRAVAILLEES', 45))
    st.session_state.config['CO2_VOITURE_G_PAR_KM'] = st.number_input("Émissions CO₂ (g/km)", value=st.session_state.config.get('CO2_VOITURE_G_PAR_KM', 120))


# --- CALCULS PRINCIPAUX ---
distance_trajet = profil_data['km_jour'] * (2 if profil_data['aller_retour'] else 1)
km_an = distance_trajet * profil_data['jours_semaine'] * st.session_state.config['SEMAINES_TRAVAILLEES']
entretien_total = profil_data['entretien_annuel'] * profil_data['duree']

resultats = calculer_couts(
    profil_data['prix_achat'], profil_data['aide'], entretien_total,
    profil_data['duree'], profil_data['fmd'], km_an
)

# --- CALCULS D'ANALYSE APPROFONDIE ---
cout_annuel_voiture = st.session_state.config['COUT_VOITURE_KM'] * km_an
economie_vs_voiture = cout_annuel_voiture - resultats['cout_annuel_fmd']
economie_vs_transport = st.session_state.config['COUT_NAVIGO_ANNUEL'] - resultats['cout_annuel_fmd']
co2_economise_kg = (km_an * st.session_state.config['CO2_VOITURE_G_PAR_KM']) / 1000

temps_rentabilite = float('inf')
if economie_vs_voiture > 0:
    cout_achat_net = profil_data['prix_achat'] - profil_data['aide']
    if cout_achat_net > 0:
        temps_rentabilite = (cout_achat_net / economie_vs_voiture) * 12 # en mois

# --- AFFICHAGE DES RÉSULTATS (PAGE PRINCIPALE) ---
st.title(f"Analyse pour le profil : {st.session_state['profil_actif']}")

st.markdown("### Indicateurs Clés Annuels")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Économie vs Voiture", f"{economie_vs_voiture:.0f} €")
col2.metric("💰 Économie vs Transports", f"{economie_vs_transport:.0f} €")
col3.metric("🌍 CO₂ économisé", f"{co2_economise_kg:.0f} kg")

if temps_rentabilite != float('inf'):
    st.info(f"📈 **Point de rentabilité vs voiture :** Votre vélo sera rentabilisé en **{temps_rentabilite:.1f} mois**.")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    afficher_camembert(profil_data['prix_achat'], profil_data['aide'], entretien_total, profil_data['fmd'], profil_data['duree'])
    afficher_graphiques(resultats)

with col2:
    afficher_tableau_details(resultats)
    mode_comparaison = st.selectbox(
        "Détail de la comparaison :",
        ["Voiture", "Transports en commun"],
        key="compare_mode_detail"
    )
    afficher_camembert_comparatif(resultats, mode_comparaison, st.session_state.config)

# --- Export Excel ---
df_export = pd.DataFrame({
    "Poste": ["Coût total", "Coût annuel", "Coût mensuel", "Coût par km", "Km annuels"],
    "Sans FMD (€)": [f"{resultats['cout_total']:.2f}", f"{resultats['cout_annuel']:.2f}", f"{resultats['cout_annuel'] / 12:.2f}", f"{resultats['cout_km']:.2f}", f"{resultats['km_an']}"],
    "Avec FMD (€)": [f"{resultats['cout_total_fmd']:.2f}", f"{resultats['cout_annuel_fmd']:.2f}", f"{resultats['cout_annuel_fmd'] / 12:.2f}", f"{resultats['cout_km_fmd']:.2f}", ""]
}).set_index('Poste')

@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Resultats RideCostCompare')
    return output.getvalue()

excel_file = to_excel(df_export)
st.download_button(
    label="📥 Exporter les résultats en Excel",
    data=excel_file,
    file_name=f"Resultats_{st.session_state['profil_actif']}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)