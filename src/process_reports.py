import re
import json
import hashlib
from pathlib import Path

def extrair_json_markdown(caminho_md: str) -> dict:
    """
    Lê um arquivo Markdown e extrai o bloco JSON logo após '> [!NOTE] JSON Output'.
    Retorna o JSON como um dict Python.
    """
    try:
        texto = Path(caminho_md).read_text(encoding='utf-8')
    except UnicodeDecodeError:
        texto = Path(caminho_md).read_text(encoding='latin-1')
    
    padrao = re.compile(r'```json\s*([\s\S]*?)\s*```', re.DOTALL)
    m = padrao.search(texto)
    if not m:
        raise ValueError("Bloco JSON não encontrado no Markdown.")
    return json.loads(m.group(1))

def consolidar_relatorios():
    """Consolida todos os relatórios .md em um único JSON"""
    reports_dir = Path('data/reports/raw')
    relatorios = []
    
    for md_file in reports_dir.glob('*.md'):
        try:
            dados = extrair_json_markdown(str(md_file))
            report_id = hashlib.md5(md_file.name.encode('utf-8', errors='replace')).hexdigest()[:12]
            
            relatorios.append({
                "id": report_id,
                "fonte": md_file.name,
                "dados": dados
            })
            
        except Exception as e:
            print(f"ERRO em {md_file.name}: {str(e)}")
    
    Path('data/reports/consolidated.json').write_text(
        json.dumps({"relatorios": relatorios}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    consolidar_relatorios()
