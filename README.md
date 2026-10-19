# Social Profile Collector

> **Local private review:** publication is paused. See [security review and remaining release conditions](docs/SECURITY_REVIEW.md). Local fixes have not been pushed.


A Python collection and monitoring toolkit combining profile/API parsing, browser automation and optional on-chain enrichment.

![review](https://img.shields.io/badge/review-private-374151) ![primary](https://img.shields.io/badge/primary-Python-2563EB) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Douglas%20Silva-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/douglas-silva-data-analyst/)

[Overview](#overview) · [Architecture](#architecture) · [Setup](#setup) · [Validation](#validation) · [Roadmap](#roadmap) · [Review notes](docs/REVIEW.md)

## Overview

- HTTP and browser collectors support different page delivery modes.
- Profile/post parsing extracts structured observations.
- Optional chain and notification scripts enrich collected events.

**Technology:** Python · requests · BeautifulSoup · lxml · Selenium · websocket-client

**Persistence and data:** Local JSON/HTML files record collected output. Previous profile snapshots, browser data and copied virtual-environment packages are excluded.

## Architecture

```text
Configured profile source → HTTP/browser collector → structured local records → optional monitoring/enrichment
```

| Location | Review focus |
| --- | --- |
| [`moltx_scraper.py`](moltx_scraper.py) | Source/configuration inspected for scope and structure |
| [`moltx_browser_scraper.py`](moltx_browser_scraper.py) | Source/configuration inspected for scope and structure |
| [`monitor.py`](monitor.py) | Source/configuration inspected for scope and structure |
| [`monitor_onchain_wss.py`](monitor_onchain_wss.py) | Source/configuration inspected for scope and structure |
| [`requirements.txt`](requirements.txt) | Source/configuration inspected for scope and structure |

Internal package and module names are retained where changing them would affect imports or compatibility. This descriptive repository name does not imply a completed package/API migration.

## Setup

Install requirements.txt in a new virtual environment. Selenium/browser setup is optional and separate. Begin with parser fixtures before any live collection.

Start from an isolated environment. Use `.env.example` when present and inspect the configuration loader: an example file is not necessarily loaded automatically. Runtime databases, real account sessions and private credentials are not bundled. Live integration prerequisites are separate from local tests.

## Validation

Static parsing checked 21 Python files and 0 strict JSON files. Python syntax errors: 0; JSON errors: 0. No functional test/build result is claimed for this preparation.

Available test scripts are inventoried in [the review notes](docs/REVIEW.md). Choose offline checks before operating any integration.

These results apply to the selected checks on the preparation copy. They do not establish deployment readiness, full coverage, live provider availability or measured performance. CI definitions, when present under `docs/ci-templates/`, are inactive review templates; no remote CI badge is claimed.

## Limits and current status

Source-specific scripts contain original investigation defaults and live connectivity checks. They were not run. No Chrome profile, private session, Telegram send or external scraping session was used.

This private snapshot is for code and portfolio review. Generated runtime material and unreviewed binary assets may be excluded. [Review notes](docs/REVIEW.md) record preparation scope, findings and outstanding validation.

## Roadmap

- [ ] Replace hardcoded profile targets with CLI/configuration inputs.
- [ ] Add sanitized HTML/JSON fixtures and parser tests.
- [ ] Separate collection from chain analysis and notification entrypoints.

## History and attribution

No recoverable original Git history was verified for this snapshot. Import and preparation commits use their actual current dates; filesystem timestamps are not treated as development dates.

No open-source license is granted by this preparation. A license and attribution review is required before public redistribution.

## Maintainer and feedback

Douglas de Oliveira Silva · [GitHub](https://github.com/qquante) · [LinkedIn](https://www.linkedin.com/in/douglas-silva-data-analyst/)

For this private review, report reproducible issues with a minimal fixture and the exact check output. Keep account data, credentials and generated sensitive reports out of issues and commits. Existing contribution guidelines apply where present.

**Topics:** `python`, `selenium`, `beautifulsoup`, `data-collection`, `web-automation`, `social-data`
