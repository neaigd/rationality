from pathlib import Path
import json
import hashlib
import time
import re

def extract_report_json(content: str) -> dict:
    """Extrai o JSON do bloco markdown usando regex"""
    json_match = re.search(
        r'```json\s*({.*?})\s*```',
        content,
        flags=re.DOTALL
    )
    
    if not json_match:
        raise ValueError("Bloco JSON não encontrado no relatório")
        
    return json.loads(json_match.group(1))

def generate_report_id(filename: str, content: str) -> str:
    """Gera ID único baseado no nome do arquivo e conteúdo"""
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', filename)[:30]
    content_hash = hashlib.md5(content.encode()).hexdigest()[:6]
    return f"{clean_name}_{content_hash}"

def main():
    reports_dir = Path('data/reports/raw')
    consolidated_path = Path('data/reports/consolidated.json')
    
    all_reports = []
    
    for md_path in reports_dir.glob('*.md'):
        try:
            content = md_path.read_text(encoding='utf-8')
            report_data = extract_report_json(content)
            
            # Gera ID único e adiciona metadados
            report_id = generate_report_id(md_path.name, content)
            report_data.update({
                "id": report_id,
                "source_file": str(md_path),
                "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Valida campos obrigatórios
            required_fields = ['analise_criterios', 'resultado_final_rc']
            if missing := [f for f in required_fields if f not in report_data]:
                raise ValueError(f"Campos obrigatórios ausentes: {missing}")
            
            all_reports.append(report_data)
        except Exception as e:
            print(f"\n=== ERRO PROCESSANDO {md_path.name} ===")
            print(f"Tipo: {type(e).__name__}")
            print(f"Detalhes: {str(e)}")
            print(f"Trecho problemático:\n{content[:200]}...\n")
            continue
    
    consolidated_path.write_text(
        json.dumps(all_reports, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"Consolidado {len(all_reports)} relatórios em {consolidated_path}")

if __name__ == '__main__':
    main()
