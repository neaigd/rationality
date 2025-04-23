import os
import re
import requests
from datetime import datetime
from io import BytesIO
from pdfminer.high_level import extract_text

def baixar_pdf(url: str) -> bytes:
    """
    Baixa o PDF de uma URL e retorna seu conteúdo em bytes.
    Utiliza requests.get com stream para downloads seguros.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    return response.content

def extrair_texto_pdf(pdf_bytes: bytes) -> str:
    """
    Extrai texto bruto de um PDF armazenado em bytes, usando pdfminer.six
    via extract_text em um BytesIO.
    """
    return extract_text(BytesIO(pdf_bytes))

def extrair_urls_do_markdown(caminho_arquivo: str) -> list:
    """
    Extrai URLs de download da tabela no arquivo markdown.
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Padrão para encontrar URLs em qualquer lugar no arquivo
    padrao = r'https?://[^\s\)\]]+'
    urls = re.findall(padrao, conteudo)
    return urls

def main():
    # Caminho para o arquivo markdown com as fontes
    caminho_markdown = 'novas_fontes/download_faça a busca confirme especifi-183019729.md'
    
    # Extrair URLs do markdown
    print(f"Lendo arquivo markdown: {caminho_markdown}")
    urls = extrair_urls_do_markdown(caminho_markdown)
    print(f"URLs encontradas: {urls}")
    if not urls:
        print("Nenhuma URL encontrada no arquivo markdown.")
        return

    # Criar diretório de saída com data atual
    data_atual = datetime.now().strftime('%Y%m%d')
    output_dir = os.path.join('output', data_atual)
    os.makedirs(output_dir, exist_ok=True)

    # Processar cada URL
    for i, url in enumerate(urls, 1):
        try:
            pdf_bytes = baixar_pdf(url)
            texto = extrair_texto_pdf(pdf_bytes)
            
            # Salvar cada artigo em arquivo separado
            filename = os.path.join(output_dir, f"article_{i}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"=== Conteúdo do PDF: {url} ===\n\n")
                f.write(texto.strip())
            print(f"Processado e salvo: {url} -> {filename}")
        except Exception as e:
            print(f"Erro ao processar {url}: {e}")

    print("Todos os artigos foram processados.")

if __name__ == "__main__":
    main()
