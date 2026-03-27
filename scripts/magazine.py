from fpdf import FPDF
import glob
import os

def generate_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Capa
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(200, 100, "The Tech - Revista Mensal", ln=True, align='C')
    
    # Busca os top 10 artigos (exemplo simplificado por data/ficheiro)
    files = glob.glob("content/articles/pt/*.md")[:10]
    
    for file in files:
        pdf.add_page()
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read().split("---")[-1] # Remove o cabeçalho Hugo
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, content)
            
    os.makedirs("static/magazine", exist_ok=True)
    pdf.output("static/magazine/revista-marco-2026.pdf")

if __name__ == "__main__":
    generate_pdf()
