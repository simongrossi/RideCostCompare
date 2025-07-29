# -*- coding: utf-8 -*-

class AppConfig:
    """
    Classe de configuration pour centraliser les paramètres de l'application.
    """
    # Paramètres généraux de l'application
    PAGE_TITLE = "RideCostCompare"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    # Constantes pour les calculs économiques et écologiques
    SEMAINES_TRAVAILLEES_PAR_AN = 45
    CO2_VOITURE_G_PAR_KM = 120  # Émissions moyennes en g/km

    # Paramètres pour les profils par défaut (vélo et voiture)
    DEFAULT_PROFIL_VELO_FILE = 'profils.json'
    
    DEFAULT_VOITURE_PARAMS = {
        "prix_achat": 20000, 
        "valeur_revente": 5000, 
        "duree_possession": 5,
        "assurance": 600, 
        "entretien": 500, 
        "autres_frais": 200,
        "km_annuels": 10000, 
        "consommation": 6.5, 
        "prix_carburant": 1.90
    }