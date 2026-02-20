from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import sqlite3

def gerar_pdf():
    doc = SimpleDocTemplate("relatorio_ocorrencias.pdf", pagesize=A4)
    elementos = []
    estilos = getSampleStyleSheet()

    conn = sqlite3.connect("ocorrencias.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ocorrencias")
    dados = cursor.fetchall()
    conn.close()

    for ocorrencia in dados:
        texto = f"ID: {ocorrencia[0]} - {ocorrencia[1]} - {ocorrencia[2]}"
        elementos.append(Paragraph(texto, estilos["Normal"]))
        elementos.append(Spacer(1, 12))

    doc.build(elementos)