import subprocess
from pathlib import Path
from typing import List
import time

def find_text_files(input_dir: Path) -> List[Path]:
    """Encontra todos os arquivos .txt no diretório de entrada"""
    return list(input_dir.glob('**/*.txt'))

def run_fabric_analysis(text_path: Path) -> str:
    """Executa análise do Fabric para um arquivo de texto"""
    cmd = [
        'sh', '-c',
        f'cat "{str(text_path)}" | fabric -sp verify_rationality_aguillar'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=True,
            timeout=300  # 5 minutos por análise
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro no Fabric: {e.stderr}")

def generate_reports():
    input_dir = Path('output')
    reports_dir = Path('data/reports/raw')
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    txt_files = find_text_files(input_dir)
    
    for i, txt_path in enumerate(txt_files):
        try:
            # Header do processamento
            current_time = time.strftime("%H:%M:%S")
            print(f"\n⚙️ PROCESSANDO ({i+1}/{len(txt_files)})")
            print(f"📄 Arquivo: {txt_path.name}")
            print(f"⏰ Início: {current_time}")
            print("🔍 Executando análise via Fabric...")
            start_time = time.time()
            
            report = run_fabric_analysis(txt_path)
            print("✅ Análise concluída com sucesso")
            
            report_path = reports_dir / f"{txt_path.stem}.md"
            report_path.write_text(report, encoding='utf-8')
            
            elapsed = time.time() - start_time
            print(f"✅ ARQUIVO SALVO: {report_path.name}")
            print(f"⏱ Tempo de processamento: {elapsed:.2f}s")
            
            # Intervalo entre requisições
            if i < len(txt_files) - 1:
                next_file = txt_files[i+1].name
                wait_seconds = 120
                print(f"\n⏳ Aguardando {wait_seconds/60} minutos para próxima análise")
                print(f"🕒 Próximo arquivo: {next_file}")
                print(f"⏱ Tempo restante total estimado: {(len(txt_files)-i-1)*2} minutos")
                
                start_wait = time.time()
                while (time.time() - start_wait) < wait_seconds:
                    remaining = wait_seconds - (time.time() - start_wait)
                    print(f"🕒 Retomando em {remaining:.0f} segundos...", end='\r')
                    time.sleep(1)
                
                print(f"\n⏰ Próxima análise iniciará em: {time.strftime('%H:%M:%S')}") 
            
        except Exception as e:
            print(f"Erro processando {txt_path.name}: {str(e)}")
            continue

if __name__ == '__main__':
    generate_reports()
