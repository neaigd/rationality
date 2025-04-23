# Estrutura do Projeto

## Diretórios Principais

- `src/`: Scripts Python do projeto
  - `extract_pdf_text.py`: Extrai texto de PDFs
  - `download_source.py`: Baixa artigos das fontes
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

## Como Usar

1. Instale as dependências: `pip install -r requirements.txt`
2. Execute os scripts conforme necessário
3. Os resultados serão salvos em `output/`
