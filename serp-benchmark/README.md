# SERP API AI Overview Parsing Fidelity Benchmark

This repository contains the benchmarking framework, data, and analysis scripts for measuring how well different SERP APIs (Search Engine Results Page Application Programming Interfaces) parse Google AI Overviews. 

Unlike most API benchmarks that focus on latency and uptime, this framework measures **parsing fidelity**: how completely, accurately, and reliably does the API extract the structured content (text blocks, citations, lists) from the non-deterministic AI Overview block?

The four providers evaluated are:
- SearchApi
- SerpApi
- Serper
- DataForSEO

## Reproducibility Setup

This repository is designed to be fully reproducible. You can run the entire benchmark and generate your own charts by following these steps.

### 1. Prerequisites
- Python 3.12+
- A Google Chrome installation (for Playwright browser automation)

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/lyd1acla1r3/serp-benchmark.git
cd serp-benchmark
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
playwright install chromium
```

### 3. Configuration
Copy the configuration template and add your API keys.

```bash
cp config.yaml.example config.yaml
```

Edit `config.yaml` to include your keys for the respective providers. The benchmark uses the free tiers for all providers (DataForSEO requires a nominal $1 trial credit).

### 4. Running the Benchmark

The execution flow consists of three phases.

**Phase 1: Build the Gold Standard (Ground Truth)**
The "gold standard" is an independent, browser-captured record of what Google actually showed for each query. Run the capture script to use a headless browser (a real browser controlled by code, with no visible window) to search Google, extract the AI Overview if present, and save a screenshot as visual proof.

```bash
python gold_standard/capture.py
```
*Note: You must manually review the output in `gold_standard/verified/` to confirm the AI Overview content was captured correctly. Queries without an AI Overview will be automatically skipped.*

**Phase 2: Execute the Benchmark Harness**
Once the gold standard is verified, run the main benchmark. This script will query all four APIs, evaluate their JSON responses against the gold standard using a strict fidelity scoring rubric, and save the raw and scored results.

```bash
python benchmark/run.py
```

**Phase 3: Generate Analysis and Charts**
Run the analyzer to aggregate scores, compute derived metrics (like cost-adjusted fidelity and failure mode taxonomy), and generate the matplotlib charts used in the article.

```bash
python analysis/analyze.py
```

The generated charts will be saved to the `analysis/charts/` directory.

## Repository Structure

- `queries.json`: The curated dataset of 50 queries spanning four intent categories.
- `gold_standard/`: Contains the Playwright capture script and the verified baseline data (JSON and screenshots).
- `benchmark/`: The core runner, provider-specific parsing modules, and the scoring rubric logic.
- `analysis/`: The script for computing aggregate metrics and generating visualizations.
- `results/`: Output directory where the raw API responses and scored runs are saved (ignored in git).
