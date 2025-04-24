import markdown2
from pathlib import Path
import shutil

def convert_md_to_html():
    # Configurar diretórios
    md_dir = Path('data/reports/raw')
    html_dir = Path('docs/assets/reports')
    html_dir.mkdir(parents=True, exist_ok=True)
    
    # Template HTML básico
    html_template = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="/css/sb-admin-2.min.css" rel="stylesheet">
    <link href="/css/academic-dashboard.css" rel="stylesheet">
    <style>
        .report-content {{
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .report-content img {{
            max-width: 100%;
        }}
    </style>
</head>
<body>
    <div class="report-content">
        {content}
    </div>
</body>
</html>
    """
    
    # Converter cada arquivo .md
    for md_file in md_dir.glob('*.md'):
        print(f"Convertendo {md_file.name} para HTML...")
        
        # Ler conteúdo Markdown
        md_content = md_file.read_text(encoding='utf-8')
        
        # Converter para HTML
        html_content = markdown2.markdown(md_content, extras=["tables", "fenced-code-blocks"])
        
        # Aplicar template
        title = md_file.stem.replace('_', ' ')
        final_html = html_template.format(title=title, content=html_content)
        
        # Salvar arquivo HTML
        html_file = html_dir / f"{md_file.name.replace('.md', '.html')}"
        html_file.write_text(final_html, encoding='utf-8')
        
        print(f"Arquivo salvo: {html_file}")

if __name__ == '__main__':
    convert_md_to_html()
