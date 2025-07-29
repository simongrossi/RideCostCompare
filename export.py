import pandas as pd
from fpdf import FPDF
from datetime import datetime


def export_excel(df: pd.DataFrame, filename: str):
    df.to_excel(filename, index=False)


def export_pdf(resultats):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "RideCostCompare - Résultats", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    for key, val in resultats.items():
        pdf.cell(0, 10, f"{key} : {val:.2f}", ln=True)

    pdf.ln(10)
    try:
        pdf.image("camembert.png", x=30, w=150)
    except:
        pdf.cell(0, 10, "(Graphique non disponible)", ln=True)

    filename = f"RideCostCompare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
