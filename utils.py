def calculer_couts(prix_achat, aide, entretien_total, duree, fmd, km_an):
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