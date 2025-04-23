# Documentação do Problema de CAPTCHA no Google Scholar

## Método Utilizado no Script

O script `pesquisa_artigos_scholar.py` utiliza a biblioteca `scholarly` para realizar buscas no Google Scholar. O fluxo principal consiste em:

1. **Configuração Inicial**:
   - Uso de proxies (recomendado mas não obrigatório)
   - Configuração de timeout (30 segundos)
   - Sistema de logging detalhado

2. **Processo de Busca**:
   - Recebe palavras-chave como entrada
   - Para cada palavra-chave:
     - Cria um delay aleatório (10-20 segundos)
     - Executa `scholarly.search_pubs()`
     - Processa os resultados

3. **Problema Identificado**:
   - O Google Scholar bloqueia requisições após alguns acessos
   - Exibe página de CAPTCHA que interrompe o scraping
   - Mesmo com proxies, o bloqueio ocorre frequentemente

## Soluções Possíveis a Serem Pesquisadas

1. **Configuração Avançada de Proxies**:
   - Rotação automática de proxies
   - Uso de serviços premium como Luminati ou Smartproxy
   - Configuração do Tor com circuitos rotativos

2. **Resolução Automática de CAPTCHA**:
   - Serviços como 2Captcha ou Anti-Captcha
   - Integração com APIs de resolução de CAPTCHA
   - Bibliotecas como `pytesseract` para CAPTCHAs simples

3. **Alternativas ao Scholarly**:
   - Uso da API oficial do Google Scholar (se disponível)
   - Bibliotecas alternativas como `serpapi`
   - Web scraping direto com Selenium e detecção de CAPTCHA

4. **Padrões de Acesso**:
   - Limitar número de requisições por hora
   - Randomização de headers HTTP
   - Simulação de comportamento humano

## Próximos Passos Recomendados

1. Testar configurações avançadas de proxy
2. Avaliar serviços pagos de resolução de CAPTCHA
3. Considerar alternativas ao scholarly
4. Implementar sistema de retry com backoff exponencial

```python
# Exemplo de código para tratamento de CAPTCHA
try:
    results = scholarly.search_pubs(query)
except CaptchaError as e:
    logger.error("CAPTCHA detectado")
    if auto_solve_captcha:
        solve_captcha()
        continue
    else:
        break
