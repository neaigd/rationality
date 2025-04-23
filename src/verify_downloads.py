import os
import PyPDF2
from pathlib import Path

def verify_pdf(filepath):
    """Verifica se um arquivo PDF pode ser lido e extrai metadados básicos"""
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return {
                'is_valid': True,
                'pages': len(reader.pages),
                'title': reader.metadata.get('/Title', ''),
                'author': reader.metadata.get('/Author', '')
            }
    except Exception as e:
        return {
            'is_valid': False,
            'error': str(e)
        }

def check_pdf_directory(pdf_dir='pdf/'):
    """Verifica todos os PDFs em um diretório"""
    pdf_dir = Path(pdf_dir)
    results = {}
    
    for pdf_file in pdf_dir.glob('*.pdf'):
        results[pdf_file.name] = verify_pdf(pdf_file)
    
    return results

def generate_report(verification_results, output_file='output/pdf_verification_report.txt'):
    """Gera um relatório simples da verificação"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Relatório de Verificação de PDFs\n")
        f.write("="*40 + "\n\n")
        
        valid_count = sum(1 for r in verification_results.values() if r['is_valid'])
        invalid_count = len(verification_results) - valid_count
        
        f.write(f"Total de PDFs verificados: {len(verification_results)}\n")
        f.write(f"PDFs válidos: {valid_count}\n")
        f.write(f"PDFs inválidos/corrompidos: {invalid_count}\n\n")
        
        if invalid_count > 0:
            f.write("Detalhes dos PDFs com problemas:\n")
            f.write("-"*40 + "\n")
            for name, result in verification_results.items():
                if not result['is_valid']:
                    f.write(f"{name}: {result['error']}\n")
            f.write("\n")
        
        f.write("Metadados dos PDFs válidos:\n")
        f.write("-"*40 + "\n")
        for name, result in verification_results.items():
            if result['is_valid']:
                f.write(f"{name}:\n")
                f.write(f"  Páginas: {result['pages']}\n")
                if result['title']:
                    f.write(f"  Título: {result['title']}\n")
                if result['author']:
                    f.write(f"  Autor: {result['author']}\n")
                f.write("\n")

if __name__ == '__main__':
    print("Verificando arquivos PDF...")
    results = check_pdf_directory()
    generate_report(results)
    print("Relatório gerado em output/pdf_verification_report.txt")
