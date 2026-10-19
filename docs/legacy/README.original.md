> Historical project notes. Paths, operational status, badges and test claims below are retained as archival reference and have not all been revalidated. Use the root README and docs/REVIEW.md for this review snapshot.

# MoltX Sniper 🎯

Scripts Python para capturar e analisar dados do perfil @lauki no MoltX.

## 📦 Instalação

```bash
pip install -r requirements.txt
```

Para o scraper com browser (opcional):
```bash
# Baixe o ChromeDriver compatível com sua versão do Chrome
# https://chromedriver.chromium.org/downloads
```

## 🚀 Uso

### 1. Teste Rápido (Recomendado para começar)

```bash
python quick_test.py
```

Este script testa diferentes métodos de acesso e mostra qual funciona melhor.

### 2. Scraper de API

```bash
python moltx_scraper.py
```

Tenta capturar dados via API REST e scraping HTML básico.

### 3. Scraper com Browser (Avançado)

```bash
python moltx_browser_scraper.py
```

Usa Selenium para capturar dados carregados via JavaScript e interceptar requisições de rede.

## 📊 Scripts Disponíveis

### `quick_test.py`
- ✅ Teste rápido de diferentes métodos
- ✅ Identifica a melhor abordagem
- ✅ Gera relatório de viabilidade

### `moltx_scraper.py`
- ✅ Tenta múltiplos endpoints da API
- ✅ Captura perfil do usuário
- ✅ Captura posts
- ✅ Faz scraping do HTML
- ✅ Detecta dados Next.js
- ✅ Salva resultados em JSON

### `moltx_browser_scraper.py`
- ✅ Usa browser real (Chrome)
- ✅ Captura dados carregados via JS
- ✅ Intercepta requisições de rede
- ✅ Identifica endpoints da API
- ✅ Salva screenshot da página

## 📁 Arquivos Gerados

- `moltx_scraper_results.json` - Dados capturados via API/HTML
- `moltx_browser_results.json` - Dados capturados via browser
- `lauki_page.html` - Página HTML completa
- `lauki_page_test.html` - Página HTML de teste
- `lauki_screenshot.png` - Screenshot da página

## 🎯 Fluxo Recomendado

1. **Execute o teste rápido:**
   ```bash
   python quick_test.py
   ```

2. **Analise os resultados** e veja qual método funcionou

3. **Use o script apropriado:**
   - Se a API funcionar → `moltx_scraper.py`
   - Se precisar de browser → `moltx_browser_scraper.py`

## 🔗 Monitor On-Chain (Base Network)

### Testar BaseScan API Primeiro

```bash
.\TESTAR_BASESCAN.bat
```

Testa se consegue conectar na API do BaseScan e buscar dados do contrato.

### Iniciar o Monitor On-Chain

```bash
.\MONITOR_ONCHAIN.bat
```

**O que o monitor faz:**
- ✅ Monitora um contrato específico na Base Network
- ✅ Detecta quando o contrato **COMPRA tokens novos** (recebe ERC-20)
- ✅ Quando detectar compra nova, **APITA 8x** com 888 Hz por 888 ms
- ✅ Mostra detalhes: token, quantidade, endereço, TX hash
- ✅ Links diretos para BaseScan e DEXScreener
- ✅ Salva histórico de todas as compras

### Contrato Monitorado

```
0xFb653a4061cE35b66e2Ba090Cf1Fabe32f294079
```

Você pode mudar o contrato ao iniciar o monitor.

### Ver Histórico de Compras

```bash
.\VER_HISTORICO.bat
```

Mostra todas as compras detectadas pelo monitor com:
- Nome e símbolo do token
- Quantidade comprada
- Timestamp da compra
- Links para verificar

### Arquivos Gerados

- `onchain_cache.json` - Cache do monitor (última TX, tokens conhecidos)
- `historico_compras.json` - Histórico de todas as compras detectadas

## 🔔 Monitor de Posts Novos (MoltX)

### Testar o Apito Primeiro

```bash
.\TESTAR_APITO.bat
```

Isso vai apitar 8x para você testar o som (888 Hz por 888 ms cada).

### Iniciar o Monitor

```bash
.\MONITOR.bat
```

**O que o monitor faz:**
- ✅ Verifica posts novos a cada 30 segundos (configurável)
- ✅ Quando detectar post novo, **APITA 8x** com 888 Hz por 888 ms
- ✅ Mostra o conteúdo do post no terminal
- ✅ Salva o último post visto para não alertar de novo
- ✅ Roda continuamente até você parar (Ctrl+C)

### Configuração

Ao iniciar o monitor, você pode:
- Manter o intervalo padrão (30s) - pressione Enter
- Ou digitar um novo intervalo em segundos (ex: 60 para 1 minuto)

### Arquivos Gerados

- `ultimo_post.json` - Armazena o ID do último post visto

## 🔍 Próximos Passos

Após capturar os dados, você pode:

1. ✅ **Monitorar posts novos** - Use o `monitor.py`
2. **Analisar a estrutura dos dados JSON**
3. **Criar dashboard de análise**
4. **Integrar com Discord/Telegram**
5. **Análise de sentimento dos posts**

## 📝 Notas

- O MoltX pode usar Next.js (dados embutidos no HTML)
- A API pode estar em `api.moltx.io` ou `moltx.io/api`
- Alguns dados podem ser carregados via JavaScript
- Use o browser scraper se os métodos simples não funcionarem
