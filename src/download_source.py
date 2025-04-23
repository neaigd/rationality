import os
import requests
from io import BytesIO
from pdfminer.high_level import extract_text

# Lista de URLs dos artigos em PDF
urls = [
    "https://www12.senado.leg.br/ril/edicoes/50/200/ril_v50_n200_p189.pdf",
    "https://www2.senado.leg.br/bdsf/bitstream/handle/id/874/R159-05.pdf?isAllowed=y&sequence=4",
    "https://www2.senado.leg.br/bdsf/bitstream/handle/id/181894/000442098.pdf?isAllowed=y&sequence=1",
    "https://www12.senado.leg.br/ril/edicoes/47/186/ril_v47_n186_p291.pdf",
    "https://etica.uazuay.edu.ec/sites/etica.uazuay.edu.ec/files/public/MIGUEL%20REALE%2C%20A%20%C3%89TICA%2C%20O%20DIREITO%20E%20A%20ECONOMIA.pdf"
]

def baixar_pdf(url: str) -> bytes:
    """
    Baixa o PDF de uma URL e retorna seu conteúdo em bytes.
    Utiliza requests.get com stream para downloads seguros :contentReference[oaicite:4]{index=4}.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    return response.content

def extrair_texto_pdf(pdf_bytes: bytes) -> str:
    """
    Extrai texto bruto de um PDF armazenado em bytes, usando pdfminer.six
    via extract_text em um BytesIO :contentReference[oaicite:5]{index=5}.
    """
    return extract_text(BytesIO(pdf_bytes))

def main():
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    for i, url in enumerate(urls, 1):
        try:
            pdf_bytes = baixar_pdf(url)
            texto = extrair_texto_pdf(pdf_bytes)
            # Save each article to a separate file
            filename = f"output/article_{i}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"=== Conteúdo do PDF: {url} ===\n\n")
                f.write(texto.strip())
            print(f"Processado e salvo: {url} -> {filename}")
        except Exception as e:
            print(f"Erro ao processar {url}: {e}")

    print("Todos os artigos foram processados.")

if __name__ == "__main__":
    main()
