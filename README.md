# Estrutura do Projeto

## Diretórios Principais

- `src/`: Scripts Python do projeto
  - `extract_pdf_text.py`: Extrai texto de PDFs
  - `download_source.py`: Baixa artigos das fontes (avaliar necessidade)
  - `gera_graf.py`: Gera visualizações
  - `pesquisa_artigos_scholar.py`: Busca no Google Scholar
  - `verify_downloads.py`: Verifica downloads

- `data/`: Dados brutos e intermediários
  - `articles.json`: Artigos coletados
  - `scholar_search_results.json`: Resultados de buscas

- `output/`: Resultados atuais da análise (textos extraídos)

- `archive/`: Análises e resultados anteriores

- `novas_fontes/`: Novos materiais para análise
  - `pdfs/`: PDFs das novas fontes

- `patterns/`: Padrões do Fabric para análise

- `pdf/`: PDFs originais do projeto

## Fluxo de Análise

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Pipeline principal:
```bash
# Gerar relatórios individuais
python src/generate_reports.py

# Consolidar dados
python src/process_reports.py

# Gerar visualizações
python src/gera_graf.py
```

3. Estrutura de arquivos:
- `data/reports/raw/`: Relatórios individuais em Markdown
- `data/reports/consolidated.json`: Dados consolidados
- `output/`: Gráficos e visualizações

4. Para atualizar o repositório:
```bash
git add .
git commit -m "Mensagem descritiva"
git push origin main
```
