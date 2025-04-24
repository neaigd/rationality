from typing import Dict, Any
import re

CRITERIA_PATTERNS = {
    "A'": {
        'historicista': r'(histórico|contexto social|contingência|construção social)',
        'universalista': r'(princípio universal|natureza humana|a-histórico|eterno)'
    },
    "Q'": {
        'técnico': r'(interpretação legal|aplicação da lei|dogmática jurídica)',
        'contextual': r'(poder social|análise crítica|contexto histórico|funções sociais)'
    },
    "C'": {
        'reflexivo': r'(limitações do estudo|pressupostos metodológicos|contexto de produção)'
    },
    "S'": {
        'pluralista': r'(diversidade de perspectivas|pluralismo|complexidade|multifatorial)'
    },
    "R'": {
        'refutação': r'(objeção|contra-argumento|crítica à|respondendo à)'
    },
    "V'": {
        'perspectiva': r'(assumimos que|reconhecemos que|limitações da perspectiva)'
    }
}

def analyze_approach(text: str) -> Dict[str, str]:
    """Analisa o critério A' (Abordagem/Posicionamento Epistêmico)"""
    historicista = len(re.findall(CRITERIA_PATTERNS["A'"]['historicista'], text, re.I))
    universalista = len(re.findall(CRITERIA_PATTERNS["A'"]['universalista'], text, re.I))
    
    status = 'Verdadeiro' if historicista > 0 or universalista > 0 else 'Falso'
    classificacao = 'Historicista' if historicista > universalista else 'Universalista' if universalista > 0 else 'Não identificado'
    
    return {
        'status': status,
        'classificacao_detalhada': classificacao,
        'justificativa': f"Abordagem {classificacao.lower()} identificada com {historicista} menções historicistas e {universalista} universalistas"
    }

def analyze_questioning(text: str) -> Dict[str, str]:
    """Analisa o critério Q' (Questionamento/Âmbito da Crítica)"""
    tecnico = len(re.findall(CRITERIA_PATTERNS["Q'"]['técnico'], text, re.I))
    contextual = len(re.findall(CRITERIA_PATTERNS["Q'"]['contextual'], text, re.I))
    
    status = 'Verdadeiro' if tecnico > 0 or contextual > 0 else 'Falso'
    tipo = 'Técnico' if tecnico > contextual else 'Contextual' if contextual > 0 else 'Ausente'
    
    return {
        'status': status,
        'classificacao_detalhada': f"Crítica {tipo.lower()}",
        'justificativa': f"Questionamento de natureza {tipo.lower()} identificado ({tecnico} termos técnicos, {contextual} contextuais)"
    }

def calculate_final_result(analise: Dict[str, Any]) -> Dict[str, str]:
    """Calcula o resultado final da Racionalidade Científica"""
    criterios_atendidos = all([v['status'] == 'Verdadeiro' for v in analise.values()])
    
    return {
        'status_geral': 'Racionalidade Científica ATENDIDA' if criterios_atendidos else 'Racionalidade Científica NÃO ATENDIDA',
        'resumo': 'Todos os critérios foram satisfeitos' if criterios_atendidos else 
                 'Falha em um ou mais critérios de racionalidade científica'
    }

import json
import re

def extract_fabric_json(output: str) -> dict:
    """Extrai o JSON da saída do Fabric com diferentes formatos"""
    # Padrão mais flexível que captura JSON mesmo com formatação irregular
    # Extrair todo o conteúdo do bloco JSON
    json_block = re.search(
        r'> \[!NOTE\] JSON Output\s*```json\s*([\s\S]*?)\s*```',  # Captura todo conteúdo do bloco
        output,
        flags=re.IGNORECASE
    )
    
    if json_block:
        json_str = json_block.group(1).strip()
        # Remover comentários e trailing commas
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)  # Remove comentários
        json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # Remove todas trailing commas
        json_str = re.sub(r'\s+', ' ', json_str)  # Normaliza espaços
        json_str = json_str.strip()  # Remove espaços no início/fim
        json_str = json_str.replace('“', '"').replace('”', '"')  # Substitui aspas curvas
        # Garantir que o JSON comece corretamente
        json_str = re.sub(r'^[\s\x00-\x1F\x7F]*{', '{', json_str)  # Remove todos caracteres não visíveis antes da abertura
        if not json_str.startswith('{'):
            json_str = '{' + json_str  # Força a abertura do JSON se faltar
        json_str = re.sub(r'[\x00-\x1F\x7F]', '', json_str)  # Remove caracteres não imprimíveis
    else:
        # Fallback para encontrar qualquer estrutura JSON
        json_match = re.search(r'(\{[\s\S]*\})', output)
        if not json_match:
            raise ValueError(f"JSON não encontrado na saída do Fabric. Trecho relevante:\n{output[:200]}...")
        json_str = json_match.group(1)
    
    try:
        import json5
        parsed = json5.loads(json_str)
        return parsed
    except json.JSONDecodeError as e:
        # Log detalhado para diagnóstico
        error_msg = f"""Erro ao decodificar JSON:
        - Arquivo: {output.splitlines()[0][:50]}...
        - Posição do erro: {e.pos}
        - Linha: {e.lineno}, Coluna: {e.colno}
        - Contexto: {e.doc[e.pos-30:e.pos+30]}
        """
        raise ValueError(error_msg) from e

def validate_fabric_json(data: dict) -> bool:
    """Valida a estrutura do JSON do Fabric com tolerância a versões"""
    required_core = {'analise_criterios', 'resultado_final_rc'}
    optional_sections = {
        'resumo_problemas', 'resumo_conclusoes',
        'resumo_propostas', 'campos_debate'
    }
    
    # Verificar núcleo obrigatório
    if not required_core.issubset(data.keys()):
        return False
    
    # Verificar pelo menos uma seção adicional
    if not any(section in data for section in optional_sections):
        return False
    
    # Validar estrutura dos critérios
    criterios = {"A'", "Q'", "C'", "S'", "R'", "V'"}
    return all(
        criterio in data['analise_criterios']
        and isinstance(data['analise_criterios'][criterio], dict)
        for criterio in criterios
    )

def analyze_content(text: str) -> Dict[str, Any]:
    """Orquestra a análise completa do texto"""
    # Simular saída realista do Fabric com JSON válido
    fabric_output = """
    # Relatório de Análise de Racionalidade Científica
    
    ## Análise dos Critérios
    
    | Critério | Status | Classificação Detalhada | Justificativa |
    |----------|--------|--------------------------|---------------|
    | A'       | ✅ Verdadeiro | Historicista | Abordagem historicista identificada com 5 menções... |
    
    ```json
    {
      "analise_criterios": {
        "A'": {"status": "Verdadeiro", "classificacao_detalhada": "Historicista", "justificativa": "Abordagem historicista identificada"},
        "Q'": {"status": "Verdadeiro", "classificacao_detalhada": "Contextual", "justificativa": "Questionamento contextual identificado"},
        "C'": {"status": "Falso", "classificacao_detalhada": "Baixa", "justificativa": "Ausência de reflexividade metodológica"},
        "S'": {"status": "Verdadeiro", "classificacao_detalhada": "Pluralista", "justificativa": "Reconhecimento de múltiplas perspectivas"},
        "R'": {"status": "Falso", "classificacao_detalhada": "Ausente", "justificativa": "Não engajamento com posições contrárias"},
        "V'": {"status": "Verdadeiro", "classificacao_detalhada": "Consciente", "justificativa": "Perspectiva explicitamente assumida"}
      },
      "resultado_final_rc": {
        "status_geral": "Racionalidade Científica ATENDIDA",
        "resumo": "Atendimento parcial dos critérios"
      }
    }
    ```
    """
    
    # Extrair e validar JSON
    analysis = extract_fabric_json(fabric_output)
    if not validate_fabric_json(analysis):
        raise ValueError("JSON do Fabric inválido ou incompleto")
    
    return analysis
