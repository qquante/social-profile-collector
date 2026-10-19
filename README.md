# Social Profile Collector

A Python collection and monitoring toolkit combining profile/API parsing, browser automation and optional on-chain enrichment.

## Features

- HTTP and browser collectors support different page delivery modes.
- Profile/post parsing extracts structured observations.
- Optional chain and notification scripts enrich collected events.

## Stack

Python · requests · BeautifulSoup · lxml · Selenium · websocket-client

Local JSON/HTML files record collected output. Previous profile snapshots, browser data and copied virtual-environment packages are excluded.

## Getting started

Install requirements.txt in a new virtual environment. Selenium/browser setup is optional and separate. Begin with parser fixtures before any live collection.

## How it works

```text
Configured profile source → HTTP/browser collector → structured local records → optional monitoring/enrichment
```

## Current limitations

Source-specific scripts contain original investigation defaults and live connectivity checks. They were not run. No Chrome profile, private session, Telegram send or external scraping session was used.

## License

No open-source license has been granted. Redistribution terms remain to be defined.
