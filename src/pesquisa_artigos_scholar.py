#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para buscar artigos no Google Scholar, filtrar por páginas e salvar.
Usa 'scholarly' para busca e 'pypdf' para contagem de páginas.
"""

import json
import time
import random
import logging
import requests
from io import BytesIO
# Use pypdf para uma contagem de páginas mais robusta
try:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
except ImportError:
    print("Erro: Biblioteca 'pypdf' não encontrada. Instale com: pip install pypdf")
    exit(1)

import argparse
from scholarly import scholarly, ProxyGenerator

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuração do Scholarly ---
# É ALTAMENTE RECOMENDADO configurar proxies para evitar bloqueios.
# Exemplo de configuração manual (substitua pelos seus proxies):
# pg = ProxyGenerator()
# success = pg.Tor_Internal(tor_ip='127.0.0.1', tor_port=9050, tor_password="your_tor_password")
# scholarly.use_proxy(pg)
# OU configure variáveis de ambiente HTTP_PROXY e HTTPS_PROXY
# scholarly.use_proxy() # Se as variáveis de ambiente estiverem configuradas

# Se não usar proxy, pode ser bloqueado rapidamente.
logger.warning("Executando sem proxies configurados explicitamente. A busca no Google Scholar pode ser bloqueada.")
scholarly.set_timeout(30)

def buscar_no_scholar(keyword, max_results=5):
    """Busca artigos no Google Scholar usando scholarly com tratamento de erro."""
    resultados = []
    logger.info(f"Iniciando busca por: '{keyword}' (max {max_results} resultados)")
    try:
        search_query = scholarly.search_pubs(keyword)
        count = 0
        while count < max_results:
            try:
                # Usar 'next' para controlar o número de resultados e timeouts
                result = next(search_query)
                if not result: # Fim dos resultados
                    break

                bib = result.bib
                title = bib.get('title', 'N/A')
                authors = bib.get('author', 'N/A')
                year = bib.get('pub_year', 'N/A') # Campo mais comum que 'year'
                url = result.get('pub_url') or bib.get('url') # Tenta pegar a URL da publicação primeiro

                if not isinstance(authors, str): # Autores podem vir como lista
                    authors = ', '.join(authors) if authors else 'N/A'

                logger.info(f"  Encontrado: '{title[:60]}...' ({year})")
                if url:
                    resultados.append({
                        "keyword": keyword,
                        "title": title,
                        "authors": authors,
                        "year": year,
                        "url": url # URL da página do artigo (pode não ser o PDF)
                    })
                else:
                     logger.warning(f"  Artigo '{title[:60]}...' sem URL principal.")

                count += 1
                # Pequeno delay entre itens para reduzir chance de bloqueio
                time.sleep(random.uniform(0.5, 1.5))

            except StopIteration:
                logger.info("  Fim dos resultados da busca para este termo.")
                break
            except Exception as e:
                logger.error(f"  Erro ao processar um resultado para '{keyword}': {e}")
                # Tenta continuar para o próximo resultado
                continue
        logger.info(f"Busca por '{keyword}' concluída. {len(resultados)} artigos com URL encontrados.")
    except Exception as e:
        logger.error(f"Erro GERAL na busca por '{keyword}': {e}. Google Scholar pode ter bloqueado o acesso.")
    return resultados

def get_pdf_url_from_result(result_data):
    """Tenta obter a URL direta do PDF a partir dos dados do scholarly."""
    # 'scholarly' às vezes fornece 'eprint_url' para o PDF
    if 'eprint_url' in result_data and isinstance(result_data['eprint_url'], str) and result_data['eprint_url'].lower().endswith('.pdf'):
        return result_data['eprint_url']
    # Às vezes a 'pub_url' já é o PDF
    if 'url' in result_data and isinstance(result_data['url'], str) and result_data['url'].lower().endswith('.pdf'):
         return result_data['url']
    # Adicione outras lógicas aqui se descobrir mais padrões na estrutura de 'result'
    return None # Retorna None se não encontrar link direto óbvio

def contar_paginas_pypdf(pdf_url):
    """Conta páginas de um PDF a partir de uma URL usando pypdf."""
    if not pdf_url or not isinstance(pdf_url, str) or not pdf_url.lower().startswith(('http://', 'https://')):
        logger.warning(f"URL inválida ou ausente para contagem de páginas: {pdf_url}")
        return None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    logger.info(f"Tentando baixar e contar páginas de: {pdf_url}")
    try:
        response = requests.get(pdf_url, headers=headers, timeout=30, stream=True, allow_redirects=True)
        response.raise_for_status() # Verifica se houve erro HTTP (4xx ou 5xx)

        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/pdf' not in content_type:
            logger.warning(f"  Conteúdo não é PDF (Content-Type: {content_type}). URL: {pdf_url}")
            # Poderia tentar analisar HTML aqui para encontrar um link .pdf, mas é complexo
            return None

        # Ler o conteúdo em memória (necessário para pypdf a partir de stream)
        # Limitar o tamanho para evitar consumo excessivo de memória
        MAX_PDF_SIZE = 50 * 1024 * 1024 # 50 MB limit
        pdf_content = BytesIO()
        downloaded_size = 0
        for chunk in response.iter_content(chunk_size=8192):
            pdf_content.write(chunk)
            downloaded_size += len(chunk)
            if downloaded_size > MAX_PDF_SIZE:
                logger.error(f"  PDF excede o limite de tamanho ({MAX_PDF_SIZE / 1024 / 1024} MB). URL: {pdf_url}")
                return None # Retorna None para PDF muito grande

        pdf_content.seek(0) # Resetar o ponteiro do BytesIO

        # Usar pypdf para ler o PDF
        try:
            reader = PdfReader(pdf_content)
            num_pages = len(reader.pages)
            logger.info(f"  Sucesso: {num_pages} páginas encontradas.")
            return num_pages
        except PdfReadError as pdf_err:
            logger.error(f"  Erro ao LER o PDF com pypdf: {pdf_err}. URL: {pdf_url}")
            return None
        except Exception as parse_err: # Captura outros erros inesperados de pypdf
             logger.error(f"  Erro inesperado ao processar PDF com pypdf: {parse_err}. URL: {pdf_url}")
             return None

    except requests.exceptions.Timeout:
        logger.error(f"  Timeout ao baixar PDF. URL: {pdf_url}")
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error(f"  Erro na requisição HTTP: {req_err}. URL: {pdf_url}")
        return None
    except Exception as e:
        logger.error(f"  Erro desconhecido em contar_paginas_pypdf: {e}. URL: {pdf_url}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Busca artigos no Google Scholar, filtra por páginas e salva.')
    parser.add_argument('-q', '--query', required=True, help='Termo principal da pesquisa (usado se keywords não for suficiente)')
    parser.add_argument('-k', '--keywords', nargs='+', required=True, help='Lista de palavras-chave para busca individual')
    parser.add_argument('-o', '--output', default='scholar_results_filtered.json', help='Arquivo JSON de saída para resultados filtrados')
    parser.add_argument('-m', '--max_results', type=int, default=5, help='Máximo de artigos a buscar por palavra-chave')
    parser.add_argument('-p', '--max_pages', type=int, default=20, help='Máximo de páginas permitido para um artigo ser incluído')
    args = parser.parse_args()

    all_found_articles = []
    filtered_articles = []

    logger.info("--- Iniciando Processo ---")
    try:
        # Busca artigos para cada palavra-chave
        for kw in args.keywords:
            # Adiciona um delay significativo *antes* de cada busca
            delay = random.uniform(10, 20)
            logger.info(f"Aguardando {delay:.1f} segundos antes da próxima busca...")
            time.sleep(delay)
            pubs = buscar_no_scholar(kw, args.max_results)
            all_found_articles.extend(pubs) # Guarda todos encontrados, mesmo sem PDF direto

        logger.info(f"\n--- Total de {len(all_found_articles)} artigos com URL encontrados. Iniciando processamento de PDFs ---")

        # Processa e filtra os artigos encontrados
        processed_urls = set() # Para evitar processar a mesma URL múltiplas vezes
        for i, pub_data in enumerate(all_found_articles):
            logger.info(f"Processando artigo {i+1}/{len(all_found_articles)}: '{pub_data['title'][:60]}...'")

            # Tentar encontrar a URL do PDF (pode ser a mesma da pub ou a eprint_url)
            pdf_url = get_pdf_url_from_result(pub_data) # Tenta obter a URL direta do PDF

            # Se não achou link direto, usa a URL principal (pode ser HTML)
            # A função contar_paginas vai tentar baixar e verificar o tipo
            if not pdf_url:
                pdf_url = pub_data.get('url')

            if pdf_url and pdf_url not in processed_urls:
                processed_urls.add(pdf_url)
                pages = contar_paginas_pypdf(pdf_url)

                if pages is not None:
                    if pages <= args.max_pages:
                        logger.info(f"  >>> Artigo ATENDE aos critérios ({pages} páginas).")
                        filtered_articles.append({**pub_data, "pdf_url_checked": pdf_url, "pages": pages})
                    else:
                        logger.info(f"  Artigo excede o limite de páginas ({pages} > {args.max_pages}).")
                else:
                     logger.info(f"  Não foi possível determinar o número de páginas para a URL: {pdf_url}")

                # Delay entre processamento de PDFs
                time.sleep(random.uniform(2, 5))
            elif pdf_url in processed_urls:
                 logger.info(f"  URL já processada anteriormente: {pdf_url}")
            else:
                 logger.warning(f"  Nenhuma URL válida encontrada para processamento.")


        logger.info(f"\n--- Processamento de PDFs concluído ---")

        # Salvar resultados filtrados
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(filtered_articles, f, ensure_ascii=False, indent=4)
            logger.info(f"Resultados filtrados salvos com sucesso em '{args.output}'. Total de {len(filtered_articles)} artigos.")
        except IOError as e:
            logger.error(f"Erro ao salvar o arquivo JSON: {e}")

    except KeyboardInterrupt:
         logger.warning("\nProcesso interrompido pelo usuário.")
    finally:
        logger.info("--- Processo Finalizado ---")

if __name__ == "__main__":
    main()
