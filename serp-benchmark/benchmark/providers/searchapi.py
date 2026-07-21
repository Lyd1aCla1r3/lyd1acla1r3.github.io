import requests
import time
from typing import Dict, Any, Optional
from .base import BaseProvider

class SearchApiProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "SearchApi"

    def search(self, query: str) -> Dict[str, Any]:
        """
        SearchApi returns `ai_overview` in the organic result or via a page_token.
        We check if a page_token is provided to fetch the full expanded result.
        """
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key
        }
        response = requests.get("https://www.searchapi.io/api/v1/search", params=params)
        response.raise_for_status()
        data = response.json()

        # If a page_token is present in ai_overview, we must fetch the full content
        if "ai_overview" in data and "page_token" in data["ai_overview"]:
            page_token = data["ai_overview"]["page_token"]
            ai_params = {
                "engine": "google_ai_overview",
                "page_token": page_token,
                "api_key": self.api_key
            }
            # The token is short-lived, fetch immediately
            ai_resp = requests.get("https://www.searchapi.io/api/v1/search", params=ai_params)
            ai_resp.raise_for_status()
            ai_data = ai_resp.json()
            # Replace the partial ai_overview with the full one
            if "ai_overview" in ai_data:
                data["ai_overview"] = ai_data["ai_overview"]

        return data

    def extract_ai_overview(self, raw_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if "ai_overview" not in raw_response:
            return {"present": False, "summary": "", "text_blocks": [], "citations": [], "related_searches": []}
            
        aio = raw_response["ai_overview"]
        
        if "error" in aio:
            return {"present": False, "summary": "", "text_blocks": [], "citations": [], "related_searches": []}
            
        # Standardize citations
        citations = []
        for ref in (aio.get("reference_links") or []):
            citations.append({
                "url": ref.get("link", ""),
                "title": "",
                "snippet": ""
            })
            
        return {
            "present": True,
            "summary": aio.get("text", aio.get("summary", "")),
            "text_blocks": aio.get("text_blocks") or [],
            "citations": citations,
            "related_searches": aio.get("follow_up_questions") or []
        }
