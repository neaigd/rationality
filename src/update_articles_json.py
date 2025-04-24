import json
from pathlib import Path

def main():
    # Caminhos dos arquivos
    consolidated_path = Path('data/reports/consolidated.json')
    articles_path = Path('data/articles.json')
    
    # Carrega relatórios consolidados
    with open(consolidated_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        consolidated = data["relatorios"]
    
    # Transforma para estrutura do dashboard
    articles = []
    for report in consolidated:
        article = {
            "article_id": report["id"],
            "fonte": report["fonte"],
            "analise_criterios": report["dados"]["analise_criterios"],
            "resultado_final_rc": report["dados"]["resultado_final_rc"]
        }
        articles.append(article)
    
    # Salva novo arquivo articles.json
    with open(articles_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"Atualizado {articles_path} com {len(articles)} artigos")

if __name__ == '__main__':
    main()
