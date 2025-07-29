import pandas as pd
from fpdf import FPDF
from datetime import datetime
from io import BytesIO

def export_excel(df: pd.DataFrame, filename: str):
    df.to_excel(filename, index=False)

def export_pdf(resultats, chart_image_bytes=None):
    """
    Génère un rapport PDF avec les résultats et un graphique optionnel.
    
    Args:
        resultats (dict): Un dictionnaire contenant les données textuelles à afficher.
        chart_image_bytes (bytes, optional): Les octets de l'image du graphique.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "RideCostCompare - Rapport de Coûts", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)

    # Affiche les résultats textuels formatés
    for key, val in resultats.items():
        if isinstance(val, (int, float)):
            # Formate joliment la clé et ajoute l'unité
            formatted_key = key.replace('_', ' ').replace('fmd', '(FMD)').capitalize()
            unit = " €" if "cout" in key or "economie" in key else " km" if "km" in key else ""
            if "co2" in key: unit = " kg CO₂"
            
            pdf.cell(0, 8, f"{formatted_key} : {val:.2f}{unit}", ln=True)

    pdf.ln(10)

    # Intègre l'image si elle est fournie
    if chart_image_bytes:
        try:
            # Crée un "fichier" en mémoire à partir des octets de l'image
            image_file = BytesIO(chart_image_bytes)
            pdf.image(image_file, x=30, w=150)
        except Exception as e:
            pdf.set_text_color(255, 0, 0) # Rouge pour l'erreur
            pdf.cell(0, 10, f"(Erreur lors de l'intégration du graphique: {e})", ln=True)
            pdf.set_text_color(0, 0, 0)
    else:
        pdf.cell(0, 10, "(Graphique de comparaison non disponible)", ln=True)

    filename = f"RideCostCompare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    
    # Retourne le nom du fichier pour le téléchargement
    return filename