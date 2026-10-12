# SERP API AI Overview Parsing Fidelity Benchmark

This directory contains the benchmarking framework, raw data, and analysis scripts for measuring how well different SERP APIs (Search Engine Results Page Application Programming Interfaces) detect and parse Google AI Overviews. The findings are published in the article [Benchmarking SERP API Fidelity for AI Overviews](https://lyd1acla1r3.github.io/blog/serp-api-benchmark.html).

Most API benchmarks focus on latency and uptime. This framework measures **parsing fidelity** instead: how reliably the API detects the non-deterministic AI Overview block, and how much of its structured content (text blocks and citations) survives extraction.

The four providers evaluated are:
- SearchApi
- SerpApi
- Serper
- DataForSEO

## Reproducibility

Google decides per query whether to serve an AI Overview, so a fresh run will return different overviews than the published run. The raw API responses from the published run are committed in `results/`, which lets anyone recompute the published numbers exactly.

### 1. Prerequisites
- Python 3.12+
- A Google Chrome installation (only needed for the gold standard capture)

### 2. Installation
The framework lives in the `serp-benchmark` directory of the portfolio repository.

```bash
git clone https://github.com/Lyd1aCla1r3/lyd1acla1r3.github.io.git
cd lyd1acla1r3.github.io/serp-benchmark
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
playwright install chromium
```

### 3. Recompute the Published Numbers

These two scripts read the committed results and need no API keys.

```bash
python analysis/analyze.py
python analysis/audit_data_integrity.py
```

`analyze.py` computes detection yield and extraction richness for each provider and regenerates the charts in `analysis/charts/` (and in the portfolio's blog image directory).

`audit_data_integrity.py` runs the silent failure audit described in the article. It sets aside error responses, sweeps every remaining response that reported no AI Overview for overview-related keys and long unparsed strings, reports both raw and error-adjusted yields, and writes the full report to `analysis/audit_report.txt`.

### 4. Run a Fresh Benchmark (Optional)

Copy the configuration template and add your API keys.

```bash
cp config.yaml.example config.yaml
```

The benchmark uses the free tiers for all providers (DataForSEO requires a nominal $1 trial credit).

**Gold standard capture.** The capture script uses a headless browser (a real browser controlled by code, with no visible window) to search Google, extract the AI Overview HTML if present, and save a full-page screenshot.

```bash
python gold_standard/capture.py
```

The published methodology does not score against these captures. Google serves different overviews to different requests, so the APIs and the local browser often see different pages. The captures were used to discover that non-determinism, and `benchmark/scoring.py` is kept for reference but marked deprecated.

**Benchmark runner.** The runner sends all 50 queries to the four APIs, waits one second before each request, retries failed requests up to three times with exponential backoff, and saves the raw and extracted results.

```bash
python benchmark/run.py
```

Then run the two analysis scripts from step 3.

## Repository Structure

- `queries.json`: The curated dataset of 50 queries spanning four intent categories.
- `benchmark/`: The runner, the provider-specific request and parsing modules, and the deprecated gold standard scoring module.
- `analysis/`: The analysis and audit scripts, the audit report, and the generated charts.
- `results/raw/`: The raw JSON response from each provider for each query (49 per provider; no raw responses were saved for one query).
- `results/extracted/`: The normalized AI Overview extraction for each query and provider.
- `gold_standard/`: The Playwright capture script. Captured pages and screenshots are not committed.
