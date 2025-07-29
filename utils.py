def calculer_couts(prix_achat, aide, entretien_total, duree, fmd, km_an):
    """
    Calcule les différents coûts liés à l'utilisation d'un vélo sur une période donnée.
    """
    cout_total = prix_achat - aide + entretien_total
    cout_total_fmd = max(cout_total - (fmd * duree), 0)
    
    cout_annuel = cout_total / duree if duree > 0 else 0
    cout_annuel_fmd = max(cout_annuel - fmd, 0)

    cout_km = cout_annuel / km_an if km_an > 0 else 0
    cout_km_fmd = cout_annuel_fmd / km_an if km_an > 0 else 0
    
    return {
        "cout_total": cout_total,
        "cout_total_fmd": cout_total_fmd,
        "cout_annuel": cout_annuel,
        "cout_annuel_fmd": cout_annuel_fmd,
        "cout_km": cout_km,
        "cout_km_fmd": cout_km_fmd,
        "km_an": km_an,
        "duree": duree
    }

def calculer_couts_voiture(params):
    """
    Calcule le coût total de possession (TCO) annuel d'une voiture.
    """
    try:
        # Amortissement annuel du véhicule
        amortissement = (params['prix_achat'] - params['valeur_revente']) / params['duree_possession'] if params['duree_possession'] > 0 else 0
        
        # Coût annuel du carburant
        cout_carburant = (params['km_annuels'] / 100) * params['consommation'] * params['prix_carburant']
        
        # Coûts fixes annuels (hors amortissement)
        cout_fixe_annuel = params['assurance'] + params['entretien'] + params['autres_frais']
        
        cout_total_annuel = amortissement + cout_carburant + cout_fixe_annuel
        
        return {
            "cout_annuel": cout_total_annuel,
            "details": {
                "Amortissement": amortissement,
                "Carburant": cout_carburant,
                "Assurance": params['assurance'],
                "Entretien": params['entretien'],
                "Autres frais": params['autres_frais']
            }
        }
    except (ZeroDivisionError, KeyError):
        # Gère les cas où une division par zéro pourrait se produire ou une clé manquerait
        return {"cout_annuel": 0, "details": {}}