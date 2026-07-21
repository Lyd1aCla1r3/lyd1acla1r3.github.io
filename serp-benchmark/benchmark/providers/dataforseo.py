import requests
import base64
from typing import Dict, Any, Optional
from .base import BaseProvider

class DataForSeoProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "DataForSEO"

    def search(self, query: str) -> Dict[str, Any]:
        """
        DataForSEO uses a POST request. The API key is usually login:password.
        """
        if ":" in self.api_key:
            login, password = self.api_key.split(":", 1)
            credentials = base64.b64encode(f"{login}:{password}".encode('utf-8')).decode('utf-8')
        else:
            # Assume it's already base64 encoded
            credentials = self.api_key
        
        headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/json'
        }
        
        # Using Google SERP API, requesting AI overview expansion
        payload = [{
            "keyword": query,
            "location_code": 2840, # US
            "language_code": "en",
            "device": "desktop",
            "expand_ai_overview": True
        }]
        
        response = requests.post("https://api.dataforseo.com/v3/serp/google/organic/live/advanced", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def extract_ai_overview(self, raw_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            tasks = raw_response.get("tasks", [])
            if not tasks: return self._empty()
            
            results = tasks[0].get("result", [])
            if not results: return self._empty()
            
            items = results[0].get("items", [])
            
            # Find the AI Overview item
            for item in items:
                if item.get("type") == "ai_overview":
                    citations = []
                    for ref in (item.get("references") or []):
                        citations.append({
                            "url": ref.get("url", ""),
                            "title": ref.get("title", ""),
                            "snippet": ref.get("snippet", "")
                        })
                    
                    # Construct text blocks from items if present
                    text_blocks = []
                    items_list = item.get("items")
                    if isinstance(items_list, list):
                        for ai_item in items_list:
                             if isinstance(ai_item, dict) and ai_item.get("type") == "text":
                                 text_blocks.append(ai_item.get("text", ""))
                    
                    if not text_blocks and item.get("markdown"):
                        text_blocks.append(item.get("markdown"))
                    
                    summary = item.get("text") or item.get("markdown") or ""
                    if not summary and not text_blocks:
                        return self._empty()
                        
                    return {
                        "present": True,
                        "summary": summary,
                        "text_blocks": text_blocks,
                        "citations": citations,
                        "related_searches": []
                    }
                    
            return self._empty()
        except Exception:
            return self._empty()
            
    def _empty(self):
        return {"present": False, "summary": "", "text_blocks": [], "citations": [], "related_searches": []}
