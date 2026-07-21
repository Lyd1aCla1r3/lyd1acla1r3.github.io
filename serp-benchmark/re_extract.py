import json
import os
from benchmark.providers.searchapi import SearchApiProvider
from benchmark.providers.serpapi import SerpApiProvider
from benchmark.providers.serper import SerperProvider
from benchmark.providers.dataforseo import DataForSeoProvider

def slugify(text: str) -> str:
    return text.replace(" ", "_")

def main():
    with open("queries.json", "r") as f:
        queries = json.load(f)

    providers = {
        "SearchApi": SearchApiProvider(""),
        "SerpApi": SerpApiProvider(""),
        "Serper": SerperProvider(""),
        "DataForSEO": DataForSeoProvider("")
    }

    os.makedirs("results/extracted", exist_ok=True)

    for item in queries:
        query = item["query"]
        intent = item["intent"]
        slug = slugify(query)

        extracted_data = {
            "query": query,
            "intent": intent,
            "scores": {}
        }

        for provider_name, provider in providers.items():
            folder_name = provider_name.lower()
            raw_path = f"results/raw/{folder_name}/{slug}.json"
            
            extracted = {"present": False, "summary": "", "text_blocks": [], "citations": [], "related_searches": []}
            if os.path.exists(raw_path):
                with open(raw_path, "r") as rf:
                    raw_resp = json.load(rf)
                try:
                    res = provider.extract_ai_overview(raw_resp)
                    if res:
                        extracted = res
                except Exception as e:
                    print(f"Error extracting {query} for {provider_name}: {e}")
            
            extracted_data["scores"][provider_name] = {
                "extracted": extracted
            }

        with open(f"results/extracted/{slug}.json", "w") as out:
            json.dump(extracted_data, out, indent=2)

if __name__ == "__main__":
    main()
