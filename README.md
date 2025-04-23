# Análise de Racionalidade Científica (Baseado em Aguillar)

## Descrição
Repositório para preparar e analisar artigos científicos quanto à sua racionalidade, utilizando uma metodologia crítico-historicista inspirada em Fernando Herren Aguillar e automação com [fabric](https://github.com/danielmiessler/fabric).

## Fluxo de Trabalho
1. **Seleção de Artigos**: Pesquisas externas com ferramentas de deep research para identificar artigos relevantes
2. **Download dos Artigos**: Utilizar `src/download_source.py` para baixar PDFs para a pasta `pdf/`
3. **Análise Automatizada**: 
   - Executar `src/run_analysis.py` (a ser criado) que usa `fabric` para:
     - Processar arquivos PDF
     - Aplicar o pattern `patterns/verify_rattionality_aguillar.md`
     - Salvar resultados em `output/`
4. **Visualização (Opcional)**: Utilizar `src/gera_graf.py` para gerar gráficos
5. **Resultados**: Analisar arquivos em `output/`

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/neaigd/rationality.git
   cd rationality
   ```
2. Crie e ative um ambiente virtual Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Instale o [fabric](https://github.com/danielmiessler/fabric#installation)

## Uso
- **Download de artigos**:
  ```bash
  python src/download_source.py --input data/articles.json --output_dir pdf/
  ```
- **Análise automatizada** (quando implementado):
  ```bash
  python src/run_analysis.py --pdf_dir pdf/ --pattern patterns/verify_rattionality_aguillar.md --output_dir output/
  ```
- **Visualização**:
  ```bash
  python src/gera_graf.py --input output/results.json --output Graficos/
  ```

## Pattern de Análise
O arquivo `patterns/verify_rattionality_aguillar.md` contém os 6 critérios refinados para avaliação:
1. A' (Abordagem/Posicionamento Epistêmico)
2. Q' (Questionamento/Âmbito da Crítica)
3. C' (Autoanálise/Reflexividade Contextual)
4. S' (Ceticismo/Abertura à Pluralidade)
5. R' (Refutação/Engajamento com Oposição) 
6. V' (Vieses/Gestão da Perspectiva)

## Estrutura de Arquivos
- `src/`: Scripts Python
- `data/`: Arquivos de dados e metadados
- `pdf/`: Artigos em PDF para análise
- `patterns/`: Padrões de análise
- `Graficos/`: Visualizações geradas
- `output/`: Resultados das análises

## Licença
[MIT](LICENSE)
