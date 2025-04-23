import os
import PyPDF2
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {str(e)}")
        return None

def process_pdfs(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    
    pdf_files = list(input_dir.glob('*.pdf'))
    print(f"Encontrados {len(pdf_files)} arquivos PDF para processar")
    
    for pdf_path in pdf_files:
        print(f"Processando: {pdf_path.name}")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            output_path = output_dir / f"{pdf_path.stem}.txt"
            with open(output_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            print(f"Texto extraído salvo em: {output_path}")

if __name__ == "__main__":
    input_directory = "novas_fontes/pdfs"
    output_directory = "output"
    
    print("Iniciando extração de texto de PDFs...")
    process_pdfs(input_directory, output_directory)
    print("Processo concluído!")
