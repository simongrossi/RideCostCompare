from dataclasses import dataclass, field
from typing import Dict

@dataclass
class CoutResultats:
    """Stocke les résultats des calculs de coût pour le vélo."""
    cout_total: float = 0.0
    cout_total_fmd: float = 0.0
    cout_annuel: float = 0.0
    cout_annuel_fmd: float = 0.0
    cout_km: float = 0.0
    cout_km_fmd: float = 0.0
    km_an: int = 0
    duree: int = 0

@dataclass
class CoutVoitureResultats:
    """Stocke les résultats du calcul de coût pour la voiture."""
    cout_annuel: float = 0.0
    details: Dict[str, float] = field(default_factory=dict)

def calculer_couts(prix_achat: int, aide: int, entretien_total: float, duree: int, fmd: int, km_an: int) -> CoutResultats:
    """
    Calcule les différents coûts liés à l'utilisation d'un vélo et retourne un objet CoutResultats.
    """
    cout_total = prix_achat - aide + entretien_total
    cout_total_fmd = max(cout_total - (fmd * duree), 0)
    
    cout_annuel = cout_total / duree if duree > 0 else 0
    cout_annuel_fmd = max(cout_annuel - fmd, 0)

    cout_km = cout_annuel / km_an if km_an > 0 else 0
    cout_km_fmd = cout_annuel_fmd / km_an if km_an > 0 else 0
    
    return CoutResultats(
        cout_total=cout_total,
        cout_total_fmd=cout_total_fmd,
        cout_annuel=cout_annuel,
        cout_annuel_fmd=cout_annuel_fmd,
        cout_km=cout_km,
        cout_km_fmd=cout_km_fmd,
        km_an=km_an,
        duree=duree
    )

def calculer_couts_voiture(params: dict) -> CoutVoitureResultats:
    """
    Calcule le coût TCO annuel d'une voiture et retourne un objet CoutVoitureResultats.
    """
    try:
        amortissement = (params['prix_achat'] - params['valeur_revente']) / params['duree_possession']
        cout_carburant = (params['km_annuels'] / 100) * params['consommation'] * params['prix_carburant']
        cout_fixe_annuel = params['assurance'] + params['entretien'] + params['autres_frais']
        cout_total_annuel = amortissement + cout_carburant + cout_fixe_annuel
        
        details = {
            "Amortissement": amortissement, "Carburant": cout_carburant,
            "Assurance": params['assurance'], "Entretien": params['entretien'],
            "Autres frais": params['autres_frais']
        }
        return CoutVoitureResultats(cout_annuel=cout_total_annuel, details=details)
        
    except (ZeroDivisionError, KeyError):
        return CoutVoitureResultats()