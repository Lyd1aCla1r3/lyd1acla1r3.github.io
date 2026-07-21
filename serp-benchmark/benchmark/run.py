import json
import yaml
import time
import sys
from pathlib import Path

# Adjust path to import providers and scoring from the same package
sys.path.append(str(Path(__file__).parent.parent))

from benchmark.providers.searchapi import SearchApiProvider
from benchmark.providers.serpapi import SerpApiProvider
from benchmark.providers.serper import SerperProvider
from benchmark.providers.dataforseo import DataForSeoProvider

def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError("config.yaml not found. Please copy config.yaml.example and add keys.")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_query_with_retry(provider, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            raw_response = provider.search(query)
            extracted = provider.extract_ai_overview(raw_response)
            return raw_response, extracted
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"      [!] {provider.name} failed after {max_retries} attempts: {e}")
                return {"error": str(e)}, {"present": False, "summary": "", "text_blocks": [], "citations": [], "related_searches": []}
            sleep_time = 2 ** attempt
            print(f"      [!] {provider.name} request failed. Retrying in {sleep_time}s...")
            time.sleep(sleep_time)

def main():
    cfg = load_config()
    api_keys = cfg.get("api_keys", {})
    b_cfg = cfg.get("config", {})
    
    root_dir = Path(__file__).parent.parent
    queries_path = root_dir / b_cfg.get("queries_path", "queries.json")
    gold_dir = root_dir / b_cfg.get("gold_standard_dir", "gold_standard/verified")
    results_dir = root_dir / b_cfg.get("results_dir", "results")
    raw_results_dir = results_dir / "raw"
    extracted_results_dir = results_dir / "extracted"
    
    raw_results_dir.mkdir(parents=True, exist_ok=True)
    extracted_results_dir.mkdir(parents=True, exist_ok=True)
    
    with open(queries_path, 'r', encoding='utf-8') as f:
        queries = json.load(f)
        
    providers = []
    if api_keys.get("searchapi") and api_keys["searchapi"] != "YOUR_SEARCHAPI_KEY_HERE":
        providers.append(SearchApiProvider(api_keys["searchapi"]))
    if api_keys.get("serpapi") and api_keys["serpapi"] != "YOUR_SERPAPI_KEY_HERE":
        providers.append(SerpApiProvider(api_keys["serpapi"]))
    if api_keys.get("serper") and api_keys["serper"] != "YOUR_SERPER_KEY_HERE":
        providers.append(SerperProvider(api_keys["serper"]))
    if api_keys.get("dataforseo") and api_keys["dataforseo"] != "YOUR_DATAFORSEO_LOGIN:YOUR_DATAFORSEO_PASSWORD":
        providers.append(DataForSeoProvider(api_keys["dataforseo"]))
        
    if not providers:
        print("No valid API keys found in config.yaml. Exiting.")
        return

    rate_limit = b_cfg.get("rate_limit_seconds", 1.0)
    
    print(f"Starting benchmark run across {len(providers)} providers...")
    
    for item in queries:
        query = item["query"]
        safe_filename = "".join([c if c.isalnum() else "_" for c in query])
        
        # Load gold standard if exists
        gold_path = gold_dir / f"{safe_filename}.json"
        if not gold_path.exists():
            print(f"[-] Skipping '{query}' (No gold standard verified data found)")
            continue
            
        with open(gold_path, 'r', encoding='utf-8') as f:
            gold_standard = json.load(f)
            
        if not gold_standard.get("has_ai_overview", False):
            print(f"[-] Skipping '{query}' (Gold standard says no AI Overview present)")
            continue
            
        print(f"[+] Benchmarking: '{query}'")
        
        query_results = {
            "query": query,
            "intent": item["intent"],
            "scores": {}
        }
        
        for provider in providers:
            time.sleep(rate_limit)
            print(f"    -> Querying {provider.name}...")
            
            raw, extracted = run_query_with_retry(provider, query, max_retries=b_cfg.get("max_retries", 3))
            
            # Save raw
            provider_raw_dir = raw_results_dir / provider.name.lower()
            provider_raw_dir.mkdir(exist_ok=True)
            with open(provider_raw_dir / f"{safe_filename}.json", 'w', encoding='utf-8') as f:
                json.dump(raw, f, indent=2)
                
            # Save extracted without fidelity score
            query_results["scores"][provider.name] = {
                "extracted": extracted
            }
            
        with open(extracted_results_dir / f"{safe_filename}.json", 'w', encoding='utf-8') as f:
            json.dump(query_results, f, indent=2)

    print("\nBenchmark run complete! Run analysis/analyze.py to view results.")

if __name__ == "__main__":
    main()
