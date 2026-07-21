import requests
from typing import Dict, Any, Optional
from .base import BaseProvider

class SerpApiProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "SerpApi"

    def search(self, query: str) -> Dict[str, Any]:
        """
        SerpApi returns the AI Overview directly, or a page_token.
        """
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key
        }
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()

        if "ai_overview" in data and "page_token" in data["ai_overview"]:
            page_token = data["ai_overview"]["page_token"]
            ai_params = {
                "engine": "google_ai_overview",
                "page_token": page_token,
                "api_key": self.api_key
            }
            ai_resp = requests.get("https://serpapi.com/search", params=ai_params)
            ai_resp.raise_for_status()
            ai_data = ai_resp.json()
            if "ai_overview" in ai_data:
                data["ai_overview"] = ai_data["ai_overview"]

        return data

    def extract_ai_overview(self, raw_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if "ai_overview" not in raw_response:
            return {"present": False, "summary": "", "text_blocks": [], "citations": [], "related_searches": []}
            
        aio = raw_response["ai_overview"]
        
        citations = []
        # SerpApi may nest them under "sources" or "references"
        sources = aio.get("sources") or aio.get("references") or []
        for src in sources:
            citations.append({
                "url": src.get("link", ""),
                "title": src.get("title", ""),
                "snippet": src.get("snippet", "")
            })
            
        return {
            "present": True,
            "summary": aio.get("summary", ""),
            "text_blocks": aio.get("text_blocks") or [],
            "citations": citations,
            "related_searches": [] # Often missing or named differently
        }
