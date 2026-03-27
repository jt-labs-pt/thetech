import pandas as pd
from deep_translator import GoogleTranslator
import os
import re

# O teu link do Google Sheets (CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRfddwTA6S-LAH1o0nwvDj1aKzdW1CLjof2WgEDrBmIJiShx5834F24ApIowUjNO7WAyWq9WI8EG4y/pub?output=csv" 

def calculate_score(text):
    words = text.split()
    if len(words) < 10: return 0 # Evita erro com células vazias
    score = 0
    # 1. Mínimo 400 palavras
    if len(words) >= 400: score += 40
    # 2. Relevância Tech
    tech_terms = ['ai', 'web', 'dev', 'cloud', 'digital', 'data', 'hardware', 'software', 'tecnologia']
    if any(term in text.lower() for term in tech_terms): score += 30
    # 3. Coerência (Palavras únicas)
    unique_ratio = len(set(words)) / len(words)
    if unique_ratio > 0.4: score += 30
    return score

def run():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Usamos códigos de 2 letras para as pastas e tradutor
        langs_map = {
            'pt': 'portuguese',
            'en': 'english',
            'es': 'spanish',
            'fr': 'french',
            'de': 'german'
        }
        
        for i, row in df.iterrows():
            content = str(row.iloc[2]) # Coluna do Conteúdo (Geralmente a 3ª na Sheet)
            title_orig = str(row.iloc[1]) # Coluna do Título
            author = str(row.iloc[4]) if len(row) > 4 else "Anónimo"
            
            score = calculate_score(content)
            
            if score >= 70:
                for code, full_name in langs_map.items():
                    # Tradução automática
                    translated_content = GoogleTranslator(source='auto', target=code).translate(content)
                    translated_title = GoogleTranslator(source='auto', target=code).translate(title_orig)
                    
                    path = f"content/articles/{code}"
                    os.makedirs(path, exist_ok=True)
                    
                    # Criar o ficheiro .md formatado para o Hugo
                    with open(f"{path}/artigo-{i}.md", "w", encoding="utf-8") as f:
                        f.write(f"---\n")
                        f.write(f"title: \"{translated_title}\"\n")
                        f.write(f"date: 2026-03-27\n")
                        f.write(f"author: \"{author}\"\n")
                        f.write(f"score: {score}\n")
                        f.write(f"---\n\n")
                        f.write(translated_content)
        print("✅ Processamento concluído com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao processar: {e}")

if __name__ == "__main__":
    run()
