# Social Profile Collector

![Language: Python](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python) ![Browser: Selenium](https://img.shields.io/badge/Browser-Selenium-555555?style=flat-square) [![License: MIT](https://img.shields.io/badge/License-MIT-555555?style=flat-square)](LICENSE)

A MoltX-oriented collection workspace combining direct HTTP attempts, HTML parsing, Selenium-based browser collection and optional on-chain enrichment.

The scripts reflect several ways of investigating the same source. They are not all interchangeable commands: a profile request, a rendered-page scrape and a transaction reader have different prerequisites and outputs.

## Select the right entrypoint

| Task | Source |
| --- | --- |
| Try profile/post endpoints and HTML fallback | [moltx_scraper.py](moltx_scraper.py) |
| Collect through a rendered browser | [moltx_browser_scraper.py](moltx_browser_scraper.py) |
| Monitor source changes | [monitor.py](monitor.py) |
| Read chain observations over HTTP / WebSocket | [monitor_onchain.py](monitor_onchain.py), [monitor_onchain_wss.py](monitor_onchain_wss.py) |
| Extract/analyze retained data | [extrair_dados.py](extrair_dados.py), [analisar_transacoes.py](analisar_transacoes.py) |

The direct scraper tries multiple endpoint shapes and records whether a response is JSON or HTML. That fallback strategy describes the implementation, not confirmation that those endpoint variants are supported today. Some diagnostic scripts retain local HTML/JSON for further inspection.

## Environment

```console
python -m venv .venv
python -m pip install -r requirements.txt
python -m py_compile moltx_scraper.py moltx_browser_scraper.py extrair_dados.py
```

Read [docs/usage.md](docs/usage.md) for operational commands and [.env.example](.env.example) for inputs. Creating an `.env` alone does not guarantee every configuration module loads it. Selenium needs its browser/driver setup; RPC enrichment needs separately configured providers.

Telegram entrypoints can send real messages. `quick_test.py` and `testar_*` files include manual integration diagnostics, so they are not an unattended offline suite. Browser state, profile snapshots and credentials should remain local; this checkout does not prove present source compatibility.

**Technology:** Python · requests · BeautifulSoup · lxml · Selenium · websocket-client

Project-authored source: [MIT](LICENSE). Third-party components retain their own notices and terms.
