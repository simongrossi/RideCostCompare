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
    cout_comparatif = None
    label_comparatif = ""

    if "Transports en commun" in mode_comparaison:
        cout_comparatif = config['COUT_NAVIGO_ANNUEL']
        label_comparatif = "Transports"
    elif "Voiture" in mode_comparaison:
        cout_comparatif = resultats['km_an'] * config['COUT_VOITURE_KM']
        label_comparatif = "Voiture"

    if cout_comparatif is not None:
        diff = cout_comparatif - resultats['cout_annuel_fmd']
        st.metric(
            label=f"Économie vs {label_comparatif}",
            value=f"{diff:.2f} € / an",
            delta_color="off" if diff == 0 else "normal"
        )

def afficher_camembert(prix_achat, aide, entretien_total, fmd, duree):
    st.markdown("### Répartition des coûts sur la durée")
    net_achat = max(prix_achat - aide, 0)
    data = {"Poste": ["Achat net (après aide)", "Entretien"], "Valeur": [net_achat, entretien_total]}
    df = pd.DataFrame(data)
    df = df[df["Valeur"] > 0]

    fig = px.pie(df, values='Valeur', names='Poste', title=f"Coûts totaux sur {duree} ans",
                 color_discrete_map={"Achat net (après aide)": "#636EFA", "Entretien": "#EF553B"})
    fig.update_traces(textinfo='percent+value+label', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    total_fmd = fmd * duree
    st.info(f"💰 Le Forfait Mobilités Durables peut réduire ce coût de **{total_fmd} €** sur la période.")

def afficher_camembert_comparatif(resultats, mode_comparaison, config):
    if mode_comparaison == "Aucun":
        return

    labels = ["Vélo (après FMD)"]
    values = [resultats['cout_annuel_fmd']]
    label_comparatif = ""

    if "Transports en commun" in mode_comparaison:
        label_comparatif = "Transports"
        values.append(config['COUT_NAVIGO_ANNUEL'])
    elif "Voiture" in mode_comparaison:
        label_comparatif = "Voiture"
        values.append(resultats['km_an'] * config['COUT_VOITURE_KM'])
    
    if label_comparatif:
        labels.append(label_comparatif)
        data = pd.DataFrame({"Mode": labels, "Coût Annuel": values})
        fig = px.pie(data, values='Coût Annuel', names='Mode', title="Répartition des coûts annuels par mode",
                     color_discrete_map={"Vélo (après FMD)": "#00CC96", "Transports": "#AB63FA", "Voiture": "#FFA15A"})
        fig.update_traces(textinfo='percent+value+label', hole=0.4)
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