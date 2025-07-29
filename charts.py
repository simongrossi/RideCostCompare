# charts.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def afficher_graphiques(resultats):
    labels = ['Coût annuel sans FMD', 'Coût annuel avec FMD']
    values = [resultats['cout_annuel'], resultats['cout_annuel_fmd']]
    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=['#636EFA', '#00CC96'])])
    fig.update_layout(title="Comparaison du coût annuel du vélo (avec/sans Forfait Mobilités Durables)", yaxis_title="€ / an")
    st.plotly_chart(fig, use_container_width=True)

def afficher_comparaison(resultats, mode_comparaison, config):
    pass

def afficher_camembert(prix_achat, aide, entretien_total, fmd, duree):
    pass

def afficher_camembert_comparatif(resultats, mode_comparaison, config, return_fig=False):
    if mode_comparaison == "Aucun":
        return go.Figure() if return_fig else None

    labels = ["Vélo (après FMD)"]
    values = [resultats['cout_annuel_fmd']]
    label_comparatif = ""

    if "Voiture" in mode_comparaison:
        label_comparatif = "Voiture"
        cout_voiture_km = config.get('COUT_VOITURE_KM', 0)
        km_an = resultats.get('km_an', 0)
        values.append(km_an * cout_voiture_km)
    
    fig = None
    if label_comparatif:
        labels.append(label_comparatif)
        data = pd.DataFrame({"Mode": labels, "Coût Annuel": values})
        fig = px.pie(data, values='Coût Annuel', names='Mode', title="Répartition des coûts annuels par mode",
                     color_discrete_map={"Vélo (après FMD)": "#00CC96", "Transports": "#AB63FA", "Voiture": "#FFA15A"})
        fig.update_traces(textinfo='percent+value+label', hole=0.4)

    if return_fig:
        return fig if fig else go.Figure()

    if fig:
        st.plotly_chart(fig, use_container_width=True)

def afficher_tableau_details(resultats):
    st.markdown("### 📊 Détail des coûts du vélo")
    data = {
        "Poste": ["Coût total", "Coût annuel", "Coût mensuel", "Coût par km"],
        "Sans FMD (€)": [
            f"{resultats['cout_total']:.2f}",
            f"{resultats['cout_annuel']:.2f}",
            f"{resultats['cout_annuel'] / 12:.2f}",
            f"{resultats['cout_km']:.2f}"
        ],
        "Avec FMD (€)": [
            f"{resultats['cout_total_fmd']:.2f}",
            f"{resultats['cout_annuel_fmd']:.2f}",
            f"{resultats['cout_annuel_fmd'] / 12:.2f}",
            f"{resultats['cout_km_fmd']:.2f}"
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)

def afficher_camembert_repartition(details: dict, title: str):
    """Affiche un camembert de la répartition des coûts."""
    if not details:
        st.warning("Données de répartition non disponibles.")
        return
    
    valid_details = {k: v for k, v in details.items() if v > 0}
    if not valid_details:
        st.info("Aucun coût à afficher dans la répartition.")
        return

    data = pd.DataFrame(list(valid_details.items()), columns=['Poste', 'Coût'])
    fig = px.pie(data, values='Coût', names='Poste', title=title, hole=0.4)
    fig.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig, use_container_width=True)

def afficher_graphique_economies_cumulees(economie_annuelle: float, duree_annees: int = 10):
    """Affiche un graphique linéaire des économies cumulées sur plusieurs années."""
    if economie_annuelle <= 0:
        st.info("Le graphique des économies cumulées n'est pas affiché car il n'y a pas d'économie annuelle.")
        return
        
    annees = list(range(1, duree_annees + 1))
    economies = [economie_annuelle * annee for annee in annees]
    
    df = pd.DataFrame({
        "Année": annees,
        "Économies cumulées (€)": economies
    })
    
    fig = px.line(df, x="Année", y="Économies cumulées (€)", title="Projection des économies sur 10 ans", markers=True)
    fig.update_layout(yaxis_title="Économies cumulées (€)")
    st.plotly_chart(fig, use_container_width=True)