# Usage

## Environment

Create and activate a Python virtual environment, then install the declared dependencies:

```console
python -m venv .venv
python -m pip install -r requirements.txt
```

Set the values documented in `.env.example` using the environment expected by the configuration modules. Creating an `.env` file alone does not guarantee it is loaded. No real credentials or account state are bundled.

## Entrypoints

Run commands from the repository root. These are operational commands, not offline tests:

| Action | Command |
| --- | --- |
| Collect profile data | `python moltx_scraper.py` |
| Use browser-based collection | `python moltx_browser_scraper.py` |
| Monitor profiles | `python monitor.py` |
| Monitor on-chain observations over HTTP | `python monitor_onchain.py` |
| Monitor on-chain observations over WebSocket | `python monitor_onchain_wss.py` |
| Extract observations | `python extrair_dados.py` |
| Analyze transactions | `python analisar_transacoes.py` |
| Inspect purchase history | `python ver_historico_compras.py` |

Scripts may prompt for input or require locally configured RPC/API access. Telegram entrypoints can send real messages when configured; they are not part of an offline smoke test. Files named `testar_*` and `quick_test.py` include manual integration diagnostics, so do not run them as an unattended unit-test suite.

The former batch wrappers only installed dependencies or launched these Python files. Installation is now documented once, and each operation has an explicit entrypoint. Browser drivers and provider access must be configured separately.
