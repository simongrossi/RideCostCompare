# RideCostCompare 🚲

**RideCostCompare** est un simulateur Streamlit permettant de **calculer et comparer le coût des déplacements** (vélo, voiture, transports en commun, etc.) en tenant compte de l'achat, de l'entretien, des aides, du nombre de kilomètres parcourus et de nombreux paramètres économiques.

---

## ✨ Fonctionnalités

- **Simulateur de coût vélo** :
  - Prix d'achat, aides, entretien annuel, amortissement, Forfait Mobilités Durables (FMD)
  - Distance quotidienne, jours par semaine, aller-retour
  - Calculs détaillés : coût total, coût annuel, coût par km
- **Simulateur de coût voiture** :
  - Prix d’achat, revente, durée de possession
  - Assurance, entretien, autres frais fixes
  - Consommation, prix carburant, km annuels
  - Estimation du coût annuel global
- **Comparaison intelligente vélo vs voiture** :
  - Affichage du gain économique annuel
  - Calcul du **point de rentabilité** (en mois)
  - Estimation des **émissions de CO₂ économisées**
- **Visualisations interactives** :
  - Graphiques en barres et camemberts avec Plotly
- **Gestion des profils vélo** :
  - Création, mise à jour, suppression, sauvegarde dans `profils.json`
- **Export des résultats** :
  - 📤 Téléchargement Excel des coûts vélo
  - (Prévu) Export PDF avec résumé graphique

---

## 📸 Aperçu

*(Ajoutez ici une capture d’écran de l’application)*

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/<votre-utilisateur>/RideCostCompare.git
cd RideCostCompare
```

### 2. Créer un environnement virtuel

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.env\Scriptsctivate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l’application

```bash
streamlit run app.py
```

---

## 📁 Structure du projet

```
.
├── app.py              # Application Streamlit
├── charts.py           # Graphiques Plotly
├── utils.py            # Fonctions de calcul vélo et voiture
├── export.py           # Fonctions d’export (Excel/PDF)
├── profils.json        # Profils vélo enregistrés
├── requirements.txt    # Dépendances Python
└── README.md           # Ce fichier
```

---

## ⚙️ Profils et paramètres

- Les profils vélo sont enregistrés dans `profils.json` et modifiables via l'interface.
- Les paramètres voiture sont modifiables dans l'onglet correspondant.

---

## 🔜 Prochaines fonctionnalités

- Export PDF enrichi avec graphiques
- Choix entre kilométrage simple et aller-retour
- Réinitialisation rapide des champs
- Projection de coûts sur plusieurs années
- Sauvegarde automatique de l’état de simulation

---

## 🧩 Dépendances principales

```
streamlit
plotly
pandas
openpyxl
fpdf
```

---

## 📃 Licence

Projet open-source. Licence à définir.
