# RideCostCompare 🚲

**RideCostCompare** est un simulateur développé avec Streamlit permettant de **calculer et visualiser en détail le coût de possession d’un vélo**. Il compare ces coûts à ceux d’autres moyens de transport comme la voiture ou les transports en commun (Navigo), et fournit des analyses financières et écologiques pour aider à la prise de décision.

---

## ✨ Fonctionnalités

- **Calcul détaillé des coûts** :
  - Achat, entretien, aide à l’achat, durée d’amortissement, Forfait Mobilités Durables (FMD).
- **Gestion complète des profils** :
  - Créez, modifiez, enregistrez ou supprimez vos profils dans l’interface. Stockage dans `profils.json`.
- **Analyse comparative personnalisable** :
  - Comparez les coûts du vélo avec ceux de la voiture ou des transports en commun.
- **Indicateurs de performance** :
  - 💰 Économie annuelle vs voiture et transports
  - 📈 Point de rentabilité (en mois)
  - 🌍 CO₂ économisé (en kg)
- **Visualisations interactives** :
  - Graphiques en barres et en camembert via Plotly
- **Export des résultats** :
  - 📤 Téléchargement Excel en un clic
  - (Prévu) 📄 Export PDF avec résumé graphique

---

## 📸 Aperçu

*(Ajoutez ici une capture d'écran de l’application en fonctionnement)*

---

## 🚀 Installation et Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/<votre-profil>/RideCostCompare.git
cd RideCostCompare
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Sous Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# Sous Windows
python -m venv venv
.env\Scriptsctivate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application Streamlit

```bash
streamlit run app.py
```

L'application s’ouvre automatiquement dans votre navigateur.

---

## 📁 Structure du Projet

```
.
├── app.py              # Application principale Streamlit
├── charts.py           # Graphiques interactifs (Plotly)
├── utils.py            # Fonctions de calcul du coût
├── export.py           # Fonctions d’export Excel et PDF
├── profils.json        # Profils utilisateurs (données modifiables)
├── requirements.txt    # Dépendances du projet
└── README.md           # Ce fichier
```

---

## ⚙️ Configuration & Profils

- Le fichier `profils.json` contient les scénarios de vélo préremplis :
  - Vélo Classique (700 €)
  - V.A.E. Standard (2500 €)
  - V.A.E. Premium (3500 €)
- Vous pouvez modifier ou ajouter des profils directement dans l’application ou en éditant ce fichier.

---

## 🔜 Prochaines fonctionnalités

- Export PDF enrichi avec graphiques intégrés.
- Camembert de comparaison entre les modes (vélo vs voiture vs Navigo).
- Ajout de la projection sur 10 ans.
- Enregistrement automatique des simulations et réinitialisation rapide des champs.

---

## 🧩 Dépendances principales

```text
streamlit
plotly
pandas
openpyxl
fpdf
```

---

## 📃 Licence

Ce projet est open-source. Licence à définir selon votre choix (MIT, GPL, etc.).
